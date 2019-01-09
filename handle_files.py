from zlib import adler32
from time import time
from random import randint
from datetime import datetime


def hash_filename():
    hashed = adler32(str(time() * randint(1, 10)))
    date = datetime.utcnow().strftime("%d%m%Y-%H%M%S")
    return str(hashed) + "-" + str(date)
