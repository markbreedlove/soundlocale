#!/bin/bash

rsync -ruptolg --checksum --delete --delay-updates \
    --exclude '.git*' \
    /home/app/soundlocale/ /srv/www/soundlocale
if [ $? -ne 0 ]; then
    >&2 echo "Could not rsync to /srv/www/soundlocale"
    exit 1
fi

python /srv/www/soundlocale/migrate.py
