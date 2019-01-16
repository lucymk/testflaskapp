import os
import requests
import tarfile
import six.moves.urllib as urllib
from pathlib import Path


class Dataset(object):
    def __init__(self, model_folder, dataset_folder, upload_folder, categories_list, logging):
        self.model_folder = model_folder
        self.model_name = "frozen_inference_graph.pb"
        self.model_path = os.path.join(self.model_folder, self.model_name)
        self.dataset_folder = dataset_folder
        self.upload_folder = upload_folder
        self.categories_list = categories_list
        self.logging = logging

    def check(self):
        self.logging.info(
            "Checking for TensorFlow model and QuickDraw dataset...")
        self.check_paths()
        self.check_model()
        self.check_binaries()

    def check_paths(self):
        for dir in [self.model_folder, self.dataset_folder, self.upload_folder]:
            if not Path(dir).exists():
                self.logging.info("Creating folder: " + dir)
                Path(dir).mkdir(parents=True)

    def check_model(self):
        if not os.path.isfile(self.model_path):
            url = "http://download.tensorflow.org/models/object_detection/"
            filename = self.model_folder.split("/")[-1] + ".tar.gz"
            self.logging.info("Downloading model file: %s", filename)
            opener = urllib.request.URLopener()
            opener.retrieve(url + filename, filename)
            tar_file = tarfile.open(filename)
            for file in tar_file.getmembers():
                file_name = os.path.basename(file.name)
                if self.model_name in file_name:
                    tar_file.extract(file, path=str(
                        Path(self.model_folder).parent))
            os.remove(filename)

    def check_binaries(self):
        files = Path(self.dataset_folder).glob('*.bin')
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

    def get_model_path(self):
        return self.model_path
