import sys
import os

def get():
    config_file = os.path.abspath('./configuration')
    if not os.path.exists(config_file):
        sys.stderr.write('Can not find configuration file')
        raise
    config = {}
    execfile(config_file, config)
    return config

