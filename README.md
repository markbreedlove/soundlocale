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
Install the binaries for transcoding Vorbis, AAC, and MP3: faac, faad, mpg123,
oggdec, and oggenc; then, install audiotools (audiotools.sourceforge.net)


To do
-----
- [x] Transcode files: need both m4a and ogg.
- [x] Web Audio API for mobile Safari support.
- [x] Progress indicators
- [ ] Add Vagrant and Ansible files to ease installation, demoing, development
- [ ] Support Gevent
- [ ] Fix login response for incorrect password.  (And ensure correct HTTP responses everywhere, in general.)
- [ ] Maps!  Geolocate uploaded sounds.  Show positions of sounds on home page.
- [ ] Main page:  list users who have sounds in the current area.  Choose which
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

    Copyright (C) 2013  Mark Breedlove (http://www.markbreedlove.com/)
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

