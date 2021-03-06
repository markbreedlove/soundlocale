# Copyright (C) Mark Breedlove and Qingyang Xi
# See README.md and License.txt.

"""
Wrapper functions for signing and unsigning strings.
"""

from itsdangerous import Signer, BadSignature
from ourexceptions import BadRequestError


def sign(s, config):
    signer = Signer(config['SIGNING_KEY'])
    try:
        return signer.sign(s)
    except BadSignature:
        raise BadRequestError()

def unsign(s, config):
    signer = Signer(config['SIGNING_KEY'])
    try:
        return signer.unsign(s)
    except BadSignature:
        raise BadRequestError()

