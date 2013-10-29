
__all__ = ['check_float', 'check_int', 'check_notempty']

def check_float(n):
    if not type(n) == float:
        raise Exception("%s is not float" % n)
    return n

def check_int(n):
    if not type(n) == int:
        raise Exception("%s is not int" % n)
    return n

def check_notempty(s):
    if len(s) == 0:
        raise Exception("got empty value")
    return s

