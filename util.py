# Copyright (C) 2013  Mark Breedlove and Qingyang Xi
# See README.md and License.txt.

"""
Common utility functions
"""

from math import sin, asin, cos, radians, pi, pow, sqrt, atan2
from threading import Thread
from flask import request

m_per_degree = 111.0 * 1000.0
R = 6371 * 1000  # Earth's radius, 6371 Km, in meters

def boundaries(lat, lon, meters):
    '''
    Return the northern, southern, western, and eastern boundaries of
    a box, given a latitude and longitude for the center point, and
    a distance from the center in meters.
    '''
    n = lat - meters / m_per_degree
    s = lat + meters / m_per_degree
    w = lon - meters / abs(cos(radians(lat)) * m_per_degree)
    e = lon + meters / abs(cos(radians(lat)) * m_per_degree)
    return {'n':n, 's':s, 'w':w, 'e':e}

def distance(lat1, lng1, lat2, lng2):
    '''
    Return the distance in meters between two points, using the
    Haversine formula.
    '''
    d_lat = radians(lat2 - lat1)
    d_lng = radians(lng2 - lng1)
    a = sin(d_lat / 2) * sin(d_lat / 2) \
            + cos(radians(lat1)) * cos(radians(lat2)) * sin(d_lng / 2) \
            * sin(d_lng / 2)
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    d = R * c
    return d

def form_or_json():
    """
    Handle JSON- or form-encoded data in a POST or PUT request.
    There's probably a better way to do this in Flask, but I don't know
    what it is, yet.
    """
    if request.content_type.startswith('application/json'):
        data = request.get_json()
    else:
        data = request.form
    return data

def async(f):
    """
    Decorator for making the given function run asynchronously
    """
    # See: http://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xi-email-support
    def wrapper(*args, **kwargs):
        t = Thread(target=f, args=args, kwargs=kwargs)
        t.start()
    return wrapper

