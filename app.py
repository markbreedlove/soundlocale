
import os
import config
from flask import Flask, jsonify, render_template, request
from nfconverter import NegativeFloatConverter
app = Flask('localsounds')
app.url_map.converters['float'] = NegativeFloatConverter
app.debug = True
cfg = config.get()

# Twisted reference: https://gist.github.com/faruken/3174638
from twisted.application import service
from twisted.web import server, static
from twisted.web.resource import Resource
from twisted.web.wsgi import WSGIResource
from twisted.internet import reactor

from models import db
from views.user import *
from views.sound import *

db.init(cfg['db_name'],
        **{'passwd': cfg['db_password'],
           'host': cfg['db_host'],
           'user': cfg['db_user']})


@app.route('/')
def index():
    return render_template('index.html')


class Root(Resource):
    """
    Root class for Twisted
    """
    wsgi = WSGIResource(reactor, reactor.getThreadPool(), app)

    def getChild(self, path, request):
        request.prepath.pop()
        request.postpath.insert(0, path)
        return self.wsgi

    def render(self, request):
        return self.wsgi.render(request)


if __name__ == '__main__':
    app.run()
else:
    # Run with Twisted
    application = service.Application('localsounds')
    root = Root()
    static_dir = os.path.join(os.path.abspath(__file__), 'static')
    resource = static.File(static_dir)
    root.putChild('static', resource)
    site = server.Site(root)

