from flask import (Flask, Response, request, jsonify)
from flask_cors import CORS

import os
from werkzeug.utils import secure_filename

from image_convert import convert_to_base64
from image_watermark import add_watermark

application = Flask(__name__)
CORS(application)
application.config.from_mapping(
    UPLOAD_FOLDER='efs/uploads',
    ALLOWED_EXTENSIONS=set(['png', 'jpg', 'jpeg'])
)
application.debug = True


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in application.config['ALLOWED_EXTENSIONS']


@application.route('/', methods=['GET'])
def hello():
    return Response("Foo bar baz")


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


if __name__ == "__main__":
    application.run()
