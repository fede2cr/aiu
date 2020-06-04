#!/usr/bin/bash

# Elimina archivos con más de 5 días de antiguedad.
# Evita que directorio spool crezca demasiado, pero da chance de depurar

find /var/spool/aiu/ -type f -mtime +5 -exec rm {} \;
find /var/spool/aiu/ -type d -mtime +5 -exec rmdir {} \;
