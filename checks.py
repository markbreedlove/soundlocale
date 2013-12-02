# Copyright (C) 2013  Mark Breedlove and Qingyang Xi
# See README.md and License.txt.

__all__ = ['check_float', 'check_int', 'check_notempty']

from ourexceptions import BadRequestError

def check_float(n):
    if not type(n) == float:
        raise BadRequestError("%s is not float" % n)
    return n

def check_int(n):
    if not type(n) == int:
        raise BadRequestError("%s is not int" % n)
    return n

def check_notempty(s):
    if len(s) == 0:
        raise BadRequestError("got empty value")
    return s

