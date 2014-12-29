# Copyright (C) 2013  Mark Breedlove and Qingyang Xi
# See README.md and License.txt.

"""
To run as a WSGI application, see gevent_wsgi.py.  This is the preferred method.

To run with Twisted handling the app plus the static resources, see
twistd_wsgi.py.

To run with passenger (e.g. in a shared hosting environment; less desirable):
    Copy passenger_wsgi.py.dist to passenger_wsgi.py and edit it with the
    path to your executable.

"""

import os
from flask import Flask, jsonify, render_template, request, session, Response
from nfconverter import NegativeFloatConverter
app = Flask('soundlocale')
app.url_map.converters['float'] = NegativeFloatConverter
config_name = os.environ.get('SOUNDLOCALE_CONFIG')
if config_name:
    app.config.from_object(config_name)
else:
    app.config.from_object('configuration')
import logging
from models import db
from views.user import *
from views.sound import *
from views.auth import *
from views.program import *

log_file_handler = logging.FileHandler(app.config['LOGFILE'])
log_file_handler.setLevel(logging.DEBUG)
app.logger.addHandler(log_file_handler)

db.init(app.config['DB_NAME'],
        **{'password': app.config['DB_PASSWORD'],
           'host': app.config['DB_HOST'],
           'user': app.config['DB_USER']})
db.connect()


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/intro')
def intro():
    return render_template('intro.html')

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

