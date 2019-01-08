import six.moves.urllib as urllib
from pathlib import Path

def download(url, filename, path):
    """download file @ specified url and save it to path"""
    fpath = Path(path) / filename
    opener = urllib.request.URLopener()
    opener.retrieve(url, "/efs/airplane.bin")
    print(fpath)
    return fpath
