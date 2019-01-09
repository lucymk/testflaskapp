from flask import (Flask, Response, request, jsonify)
from flask_cors import CORS

import os
from werkzeug.utils import secure_filename

from image_convert import convert_to_base64
from image_watermark import add_watermark

from test_download import download

from pathlib import Path

import six.moves.urllib as urllib
import tarfile

application = Flask(__name__)
CORS(application)
application.config.from_mapping(
    UPLOAD_FOLDER='/efs',
    MODEL_FOLDER='/efs/downloads/detection_models/ssd_mobilenet_v1_coco_2017_11_17',
    DATASET_FOLDER='efs/downloads/drawing_dataset',
    ALLOWED_EXTENSIONS=set(['png', 'jpg', 'jpeg'])
)
application.debug = True

for dir in [application.config["MODEL_FOLDER"], application.config["DATASET_FOLDER"]]:
    if not Path(dir).exists():
            Path(dir).mkdir(parents=True)

if not os.path.isfile(os.path.join(application.config["MODEL_FOLDER"], "frozen_inference_graph.pb")):
    url = "http://download.tensorflow.org/models/object_detection/"
    filename = "ssd_mobilenet_v1_coco_2017_11_17.tar.gz"
    application.logger.info("Downloading model file: %s", filename)
    opener = urllib.request.URLopener()
    opener.retrieve(url + filename, filename)
    tar_file = tarfile.open(filename)
    for file in tar_file.getmembers():
        file_name = os.path.basename(file.name)
        if 'frozen_inference_graph.pb' in file_name:
            tar_file.extract(file, path=str(Path(application.config["MODEL_FOLDER"]).parent))

files = Path("downloads", "drawing_dataset").glob('*.bin')
categories = [f.stem for f in files]

if not categories:
    category_list = ["aircraft carrier", "airplane", "alarm clock"]
    source = "https://storage.googleapis.com/quickdraw_dataset/full/binary/"
    for category in category_list:
        application.logger.info("Downloading dataset file: %s", category)
        download(source + category + ".bin", category + ".bin", application.config["DATASET_FOLDER"])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in application.config['ALLOWED_EXTENSIONS']

@application.route('/', methods=['GET'])
def hello():
    return Response("Foo bar baz12323")


@application.route('/upload', methods=['GET', 'POST'])
def upload():

    if request.method == 'GET':
        return Response("I'm here!")

    if request.method == 'POST':
        if 'file' not in request.files:
            return Response("You didn't send any file.")

        file = request.files['file']

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            path = os.path.join(application.config['UPLOAD_FOLDER'], filename)

            file.save(path)
            file.close()
            # # cartoon_path = cartoonify(path)
            watermark_path = os.path.join(str(path) + "_watermark.png")
            add_watermark(str(path), os.path.join(
                application.root_path, "eu-compliant-watermark.png"), watermark_path)

            return jsonify(status=200, base64=convert_to_base64(str(watermark_path)))

@application.route("/bin/<filename>")
def bin(filename=None):
    # print the current directory here
    path = os.path.join(application.config["DATASET_FOLDER"], filename + ".bin")
    abspath = os.path.abspath(path)
    if os.path.isfile(path):
        return str(abspath)
    else:
        return "FALSE " + str(abspath) 

if __name__ == "__main__":
    # /opt/python/bundle/7/app/airplane.bin > default save location if no path
    # /opt/python/bundle/9/app/downloads/airplane.bin - is FALSE
    application.run()
