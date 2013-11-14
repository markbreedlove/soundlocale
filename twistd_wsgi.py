# Copyright (C) 2013  Mark Breedlove and Tom Xi
# See README.md and License.txt.

"""
For running with the Twisted web server, with Twisted handling all of the
static assets in /static.

$ cd <this directory>
$ twistd -n web --port 8080 --wsgi twistd_wsgi.app.app
"""

# Twisted reference: https://gist.github.com/faruken/3174638
from twisted.application import service
from twisted.web import server, static
from twisted.web.resource import Resource
from twisted.web.wsgi import WSGIResource
from twisted.internet import reactor
import os
import app


class Root(Resource):
    """
    Root class for Twisted
    """
    wsgi = WSGIResource(reactor, reactor.getThreadPool(), app.app)

    def getChild(self, path, request):
        request.prepath.pop()
        request.postpath.insert(0, path)
        return self.wsgi

    def render(self, request):
        return self.wsgi.render(request)


application = service.Application('soundlocale')
root = Root()
static_dir = os.path.join(os.path.abspath(__file__), 'static')
resource = static.File(static_dir)
root.putChild('static', resource)
site = server.Site(root)


