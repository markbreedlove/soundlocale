# Copyright (C) 2013  Mark Breedlove
# See README.md and License.txt.

__all__ = ['BadRequestError', 'ConflictError', 'ForbiddenError']

class BadRequestError(Exception):
    pass

class ConflictError(Exception):
    pass

class ForbiddenError(Exception):
    pass

