# Copyright (C) 2013  Mark Breedlove and Tom Xi
# See README.md and License.txt.

"""
To run with Twisted handling the app plus the static resources, see
twistd_wsgi.py.

To run with Twisted acting as middleware between the app and a webserver:
    1.  Run Twisted like this:
        $ cd <this directory>
        $ twistd web --port 8080 --wsgi app.app --log /path/to/twistd.log
    2.  Configure your webserver to reverse-proxy the application (see your
        webserver's documentation) to the port used above, and configure it
        to alias '/static' to the 'static' directory in the app.

To run with passenger:
    Copy passenger_wsgi.py.dist to passenger_wsgi.py and edit it with the
    path to your executable.

To run with built-in Flask server:
    $ cd <this directory>
    $ python app.py
"""

import os
from flask import Flask, jsonify, render_template, request, session, Response
from nfconverter import NegativeFloatConverter
app = Flask('soundlocale')
app.url_map.converters['float'] = NegativeFloatConverter
app.config.from_object('configuration')
import logging
from models import db
from views.user import *
from views.sound import *
from views.auth import *

log_file_handler = logging.FileHandler(app.config['LOGFILE'])
log_file_handler.setLevel(logging.DEBUG)
app.logger.addHandler(log_file_handler)

db.init(app.config['DB_NAME'],
        **{'passwd': app.config['DB_PASSWORD'],
           'host': app.config['DB_HOST'],
           'user': app.config['DB_USER']})
db.connect()


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup')
def signup():
    if 'foo' in session:
        val = session['foo']
    else:
        val = 'nothing'
    return render_template('signup.html', val=val)

@app.route('/login')
def login():
    return render_template('login.html')

if __name__ == '__main__':
    app.run()

