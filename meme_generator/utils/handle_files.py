from zlib import adler32
from time import time
from random import randint
from datetime import datetime
from os import path, remove


def hash_filename(location):
    hashed = adler32(str(time() * randint(1, 10)))
    date = datetime.utcnow().strftime("%d%m%Y-%H%M%S")
    return path.join(location, str(hashed) + "-" + str(date))


def get_extension(filename):
    return filename.split(".")[-1]


def cleanup_files(files):
    for file in files:
        if path.exists(str(file)):
            remove(str(file))


def get_hash_from_filename(filename):
    return filename.split(".")[0]


def get_filename_from_hash(hashed, ext):
    ext = ext.replace(".", "")
    return ".".join([hashed, ext])


def check_hash_exists(hashed, allowed_extensions, folder):
    for extension in allowed_extensions:
        filename = get_filename_from_hash(hashed, extension)
        search_path = path.join(folder, filename)
        if path.exists(search_path):
            return search_path

    return False
