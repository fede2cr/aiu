"""
AIU, Alfresco instant uploader

Esta herramienta se encarga de descargar correos vía Imap,
procesarlos para extraer los archivos que lo componen y el
cuerpo del correo, empaquetarlos en archivo ZIP, y luego
subirlos hacia Alfresco usando webdav como monta de sistema
de archivos.
Para su uso, se recomienda integrar con cron de Unix, así
como una segunda tarea, encargada de borrar archivos y directorios
viejos en la carpeta WORKDIR.

Copyright 2020, Greencore Solutions SRL

Bajo licencia GPLv3
"""

import secrets
import email
import uuid
import imaplib
import os
import shutil

def sanitize(inputstr):
    """
    Para limpiar el subject al entrar un correo, para evitar un caso de
    inyección de comandos, como "Subject: hola; sudo poweroff"
    """
    sanitized = inputstr
    badstrings = [
        ';',
        '?',
        '=',
        '@',
        ':',
        '/',
        '$',
        '&&',
        '../',
        '<',
        '>',
        '%3C',
        '%3E',
        '\'',
        '--',
        '1,2',
        '\x00',
        '`',
        '(',
        ')',
        'file://',
        'input://'
    ]
    for badstr in badstrings:
        if badstr in sanitized:
            sanitized = sanitized.replace(badstr, '')
    return sanitized


mail = imaplib.IMAP4_SSL(secrets.email_server, '993')
mail.login(secrets.email_username, secrets.email_password)
mail.select('INBOX/aiu')

typ, data = mail.search(None, 'ALL')

mail_ids = data[0]
id_list = mail_ids.split()

WORKDIR = "/tmp/aiu"

for num in data[0].split():
    typ, data = mail.fetch(num, '(RFC822)')
    raw_email = data[0][1]

    raw_email_string = raw_email.decode('utf-8')
    email_message = email.message_from_string(raw_email_string)# downloading attachments
    WORK_ID = str(uuid.uuid4()) + "/"
    DIR_ID = WORKDIR + str(uuid.uuid4()) + "/"
    os.mkdir(DIR_ID)
    for part in email_message.walk():
        if part.get_content_maintype() == 'multipart':
            continue
        if part.get('Content-Disposition') is None:
            continue
        fileName = part.get_filename()
        if bool(fileName):
            filePath = os.path.join(DIR_ID, fileName)
            print(filePath)
            if not os.path.isfile(filePath):
                fp = open(filePath, 'wb')
                fp.write(part.get_payload(decode=True))
                fp.close()
            subject = str(email_message).split("Subject: ", 1)[1].split("\nTo:", 1)[0]

    for response_part in data:
        if isinstance(response_part, tuple):
            msg = email.message_from_string(response_part[1].decode('utf-8'))
            if msg['subject'] is not None:
                email_subject = sanitize(msg['subject'])
            else:
                email_subject = "Sin título-" + str(uuid.uuid4())
            email_from = sanitize(msg['from'])
            email_body = msg.get_payload(decode=True)
            print('From : ' + email_from + '\n')
            print('Subject : ' + email_subject + '\n')
            if email_body is not None:
                print(email_body)
                body = open(DIR_ID + "correo.txt", 'wb')
                body.write(email_body)
                body.close()
    shutil.make_archive(WORKDIR + email_subject, 'zip', DIR_ID)
    mail.store(num, '+FLAGS', '\\Deleted')

mail.expunge()
mail.logout()
