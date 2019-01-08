import six.moves.urllib as urllib
from pathlib import Path

def download(url, filename, path):
    """download file @ specified url and save it to path"""
    if not Path(path).exists():
        Path(path).mkdir()
    fpath = Path(path) / filename
    opener = urllib.request.URLopener()
    opener.retrieve(url, str(fpath))
    return fpath
