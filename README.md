# aiu
Alfresco Imap Uploader

## Usage

1. Create a file called secrets.txt with conect similar to:

```
email_username="someuser@greencore.co.cr"
email_password="password"
email_server="imap.greencore.co.cr"
```

2. Run the file with crontab, something like 5 minutes seems a good idea.
3. Delete zip files created that weight exactly 102 bytes.

## TODO

- For now, empty zip files can be created if the email has no body and no attatchments. To fix this, in the crontab erase zip files that weight exactly 102 bytes.
- Better UTF-8 and ISO encodings for the subject, since this generates the filename.
