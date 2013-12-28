# Copyright (C) 2013  Mark Breedlove and Qingyang Xi
# See README.md and License.txt.

__all__ = ['BadRequestError', 'ConflictError', 'ForbiddenError',
        'UnauthorizedError', 'NotFoundError']

from flask import jsonify
from app import app


class HTTPError(Exception):
    status_code = 500
    message = 'Internal Server Error'

    def __init__(self, message=None, status_code=None, payload=None):
        Exception.__init__(self)
        if message is not None:
            self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv


class BadRequestError(HTTPError):
    status_code = 400
    message = 'Bad Request'


class UnauthorizedError(HTTPError):
    status_code = 401
    message = 'Unauthorized'


class ForbiddenError(HTTPError):
    status_code = 403
    message = 'Forbidden'


class NotFoundError(HTTPError):
    status_code = 404
    message = 'Not Found'


class ConflictError(HTTPError):
    status_code = 409
    message = 'Conflict'


@app.errorhandler(HTTPError)
def handle_http_error(error):
    response = jsonify(error.to_dict())
    response.status = "%s %s" % (error.status_code, error.message)
    return response

