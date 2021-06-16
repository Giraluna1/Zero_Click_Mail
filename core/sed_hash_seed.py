#!/usr/bin/env python3
import os
import sys
import hashlib

def hash_id(email):
    """ this function create hash unique for each email recipient """
    if __name__ == '__main__':
    # Set hash seed and restart interpreter.
    # This will be done only once if the env var is clear.
        if not os.environ.get('PYTHONHASHSEED'):
            os.environ['PYTHONHASHSEED'] = '654321'
            os.execv(sys.executable, ['python3'] + sys.argv)

    result = hashlib.md5(email.encode())
    return result.hexdigest()
    #return hash(email)

