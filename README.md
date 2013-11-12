Soundlocale
===========


Dependencies
------------
Install the following Python packages with pip:  flask, peewee, MySQLdb,
mysql-python twisted, simpleflake, flask_mail

To do
-----
- [ ] Web Audio API for mobile Safari (et al?) support.
- [ ] Main page:  list users who have sounds in the current area.  Choose which
  user to listen to.
- [ ] User list page:  Show users, click on user & see map of sounds.
- [ ] Maps!  Develop main page, which is temporary.

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

