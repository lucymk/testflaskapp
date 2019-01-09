import os
import requests
import tarfile
from pathlib import Path
import six.moves.urllib as urllib


class Dataset(object):
    def __init__(self, model_folder, dataset_folder, categories_list, logging):
        self.model_folder = os.path.join(
            model_folder, "frozen_inference_graph.pb")
        self.dataset_folder = dataset_folder
        self.categories_list = categories_list
        self.logging = logging

    def check(self):
        self.logging.info(
            "Checking for TensorFlow model and QuickDraw dataset...")
        self.check_paths()
        self.check_model()
        self.check_binaries()

    def check_paths(self):
        for dir in [self.model_folder, self.dataset_folder]:
            if not Path(dir).exists():
                Path(dir).mkdir(parents=True)

    def check_model(self):
        if not os.path.isfile(self.model_folder):
            url = "http://download.tensorflow.org/models/object_detection/"
            filename = "ssd_mobilenet_v1_coco_2017_11_17.tar.gz"
            self.logging.info("Downloading model file: %s", filename)
            opener = urllib.request.URLopener()
            opener.retrieve(url + filename, filename)
            tar_file = tarfile.open(filename)
            for file in tar_file.getmembers():
                file_name = os.path.basename(file.name)
                if 'frozen_inference_graph.pb' in file_name:
                    tar_file.extract(file, path=str(
                        Path(self.model_folder).parent))
            os.remove(filename)

    def check_binaries(self):
        files = Path("downloads", "drawing_dataset").glob('*.bin')
        categories = [f.stem for f in files]

        if not categories:
            category_list = self.read_categories()
            source = "https://storage.googleapis.com/quickdraw_dataset/full/binary/"
            for category in category_list:
                self.logging.info(
                    "Downloading dataset file: %s", category)
                self.download(source + category + ".bin", category +
                              ".bin", self.dataset_folder)

    def read_categories(self):
        with open(self.categories_list) as f:
            categories = f.read().splitlines()
        return categories

    def download(self, url, filename, path):
        """download file @ specified url and save it to path"""

        if not Path(path).exists():
            Path(path).mkdir(parents=True)

        Path.touch(Path(path) / filename)
        abspath = Path(path) / filename

        response = requests.get(url)
        if response.status_code == 200:
            with open(str(abspath), 'wb') as f:
                f.write(response.content)

        return response.status_code
