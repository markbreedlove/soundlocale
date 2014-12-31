#!/bin/bash

# Run as root.
# Copies directory owned by `vagrant' into directory owned
# by `app'

if [ ! -d /vagrant ]; then
    echo "Local directory /vagrant does not exist" >&2
    exit 1
fi

if [ ! -d /home/app/soundlocale ]; then
    mkdir /home/app/soundlocale
fi

rsync -ruptl --delete --checksum \
    --exclude='.git*' --exclude='.vagrant' --exclude='*.pyc' \
    --exclude='configuration*' --exclude='static/storage' \
    /vagrant/ /home/app/soundlocale
if [ $? -ne 0 ]; then
    >&2 echo "Could not rsync to /home/app/soundlocale"
    exit 1
fi

chown -Rh app:app /home/app/soundlocale
