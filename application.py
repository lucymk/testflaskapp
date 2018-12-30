from flask import (Flask, Response, request, jsonify)

import os
from werkzeug.utils import secure_filename

from image_convert import convert_to_base64
from image_watermark import add_watermark

application = Flask(__name__)
application.debug = True


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in application.config['ALLOWED_EXTENSIONS']


@application.route('/', methods=['GET'])
def hello():
    resp = Response("Foo bar baz")
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


@application.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        if 'file' not in request.files:
            resp = Response("You didn't send the file.")
            resp.headers['Access-Control-Allow-Origin'] = '*'
            return resp

        file = request.files['file']

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            path = os.path.join(
                application.instance_path, application.config['UPLOAD_FOLDER'], filename)
            print(path)
            print("Going to upload the file now!")

            file.save(path)
            file.close()
            # cartoon_path = cartoonify(path)
            watermark_path = os.path.join(str(path) + "_watermark.png")
            add_watermark(str(path), os.path.join(
                application.root_path, "eu-compliant-watermark.png"), watermark_path)

            print("Going to send a response now!")
            resp = Response(jsonify(status=200, base64=convert_to_base64(str(watermark_path)))
                            )
            resp.headers['Access-Control-Allow-Origin'] = '*'
            return resp


if __name__ == "__main__":
    application.run()
