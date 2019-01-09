import os
from flask import (Flask, Response, request, jsonify)
from flask_cors import CORS
from werkzeug.utils import secure_filename
from image_convert import convert_to_base64
from image_watermark import add_watermark
from get_dataset import Dataset
from cartoonify import cartoonify
from handle_files import hash_filename


application = Flask(__name__)
CORS(application)
application.config.from_mapping(
    UPLOAD_FOLDER='uploads',
    MODEL_FOLDER='downloads/detection_models/ssd_mobilenet_v1_coco_2017_11_17',
    DATASET_FOLDER='downloads/drawing_dataset',
    ALLOWED_EXTENSIONS=set(['png', 'jpg', 'jpeg'])
)
application.debug = True

dataset = Dataset(application.config['MODEL_FOLDER'],
                  application.config["DATASET_FOLDER"], "categories.txt", logging=application.logger)
dataset.check()


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
            cartoon_path = cartoonify(
                path, application.config["DATASET_FOLDER"], application.config["MODEL_FOLDER"])
            watermark_path = os.path.join(
                application.config['UPLOAD_FOLDER'], hash_filename() + ".png")
            add_watermark(str(cartoon_path), os.path.join(
                application.root_path, "eu-compliant-watermark.png"), watermark_path)
            os.remove(path)
            os.remove(str(cartoon_path))

            return jsonify(status=200, base64=convert_to_base64(str(watermark_path)))


@application.route("/bin/<filename>")
def bin(filename=None):
    # print the current directory here
    path = os.path.join(
        application.config["DATASET_FOLDER"], filename + ".bin")
    abspath = os.path.abspath(path)
    if os.path.isfile(path):
        return str(abspath)
    else:
        return "FALSE " + str(abspath)


if __name__ == "__main__":
    # /opt/python/bundle/7/app/airplane.bin > default save location if no path
    # /opt/python/bundle/9/app/downloads/airplane.bin - is FALSE
    application.run()
