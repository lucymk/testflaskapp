import requests
from pathlib import Path

def download(url, filename, path):
    """download file @ specified url and save it to path"""

    if not Path(path).exists():
        print("mkdir")
        Path.mkdir(Path(path))

    Path.touch(Path(path) / filename)
    abspath = Path(path) / filename

    response = requests.get(url)
    if response.status_code == 200:
        with open(str(abspath), 'wb') as f:
            f.write(response.content)
    
    return response.status_code
