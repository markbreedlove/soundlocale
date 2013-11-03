from itsdangerous import Signer


def sign(s, config):
    signer = Signer(config['SIGNING_KEY'])
    return signer.sign(s)

def unsign(s, config):
    signer = Signer(config['SIGNING_KEY'])
    return signer.unsign(s)

