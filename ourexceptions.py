__all__ = ['BadRequestError', 'ConflictError', 'ForbiddenError']

class BadRequestError(Exception):
    pass

class ConflictError(Exception):
    pass

class ForbiddenError(Exception):
    pass

