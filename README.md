Soundlocale
===========

Soundlocale is a web application for playing a mix of geotagged sounds based on
the listener's present coordinates.  As the listener travels through a space,
the sounds adjust in volume based on their proximity.

This project was proposed at the September, 2013 Hacking Arts conference in
Cambridge, MA by Qingyang Xi, and has been developed thus far by Mark Breedlove.


Dependencies
------------

Install the dependencies in requirements.txt:
```
$ pip install -r requirements.txt
```

Soundlocale relies on `avconv`, which is part of the `Libav` fork of `ffmpeg`.
On Debian / Ubuntu, this is part of the `libav-tools` package.  You will also
need the `libvo-aacenc0` package for transcoding AAC.  See the provided Vagrant /
VirtualBox VM, which runs Ubuntu 14.01 and resolves all of the dependencies.

Testing and Development with Vagrant
------------------------------------
See README-vagrant.txt.  With the included Vagrant and Ansible files, you can
easily spin up virtual machines that are configured to serve up this
application.


To do
-----
- [x] Transcode files: need both m4a and ogg.
- [x] Web Audio API for mobile Safari support.
- [x] Progress indicators
- [x] Add Vagrant and Ansible files to ease installation, testing, development
- [x] Support Gevent
- [x] Fix login response for incorrect password.
- [x] Maps!  Geolocate uploaded sounds.  Show positions of sounds on home page.
- [x] Main page:  list users who have sounds in the current area.  Choose which
  user to listen to.
- [ ] User list page:  Show users, click on user & see map of sounds.
- [ ] Cloud storage
- [ ] Asynchronous transcoding

The future
----------
* A user will create programs, which are just metadata pages that can be used
  to group sounds together and give synopses.
* A next iteration may incorporate compass heading, but that seems to require
  that the device be moving.  With heading, the sounds could be panned, but
  that should be governed by an attribute of the sound.

License
-------

    Copyright (C) Mark Breedlove (http://www.markbreedlove.com/)
    and Qingyang Xi

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

