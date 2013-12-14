#!/bin/sh

VERSION="2.20"
URL="http://sourceforge.net/projects/audiotools/files/audiotools/$VERSION/audiotools-$VERSION.tar.gz/download"
ARCHIVE="audiotools-$VERSION.tar.gz"

export PATH=/bin:/usr/bin:/usr/local/bin
cd /var/tmp

download_audiotools() {
    curl -s -L -o $ARCHIVE $URL && tar zxf $ARCHIVE
}

install_audiotools() {
    dir=/var/tmp/audiotools-$VERSION
    cd $dir && make -s install && cd /var/tmp && rm -rf $dir $ARCHIVE
}


python -m audiotools.vorbis 2>/dev/null

if [ $? -eq 0 ]; then
    exit 0
else
    download_audiotools
    install_audiotools
fi

