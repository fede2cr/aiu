#!/usr/bin/env bash

# Descarga correos y convierte en ZIP
/usr/bin/python3 /usr/local/aiu/aiu.py

# Elimina zips vacíos
find /var/spool/aiu/ -name \*\.zip -size 102c -exec rm {} \;

# Mueve zips con contenido a carpeta de WebDAV
find /var/spool/aiu/ -name \*\.zip -size 102c -exec mv {} /var/spool/ventanilla \;
