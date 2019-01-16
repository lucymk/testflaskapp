from flask import (current_app, Blueprint, request,
                   url_for, redirect, send_from_directory, jsonify, abort)
import os
from cartoonify import cartoonify
from werkzeug.utils import secure_filename
from .image_convert import convert_to_base64
from .image_watermark import add_watermark
from utils.handle_files import hash_filename, cleanup_files, get_extension, get_filename_from_hash, check_hash_exists
from utils.handle_images import HandleImage

# import application context and declare new blueprint
app = current_app
bp = Blueprint('api', __name__)


def allowed_file(filename):
    """Check file extension being uploaded is allowed within the application factory setup"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


@bp.route("/fetch/<string:fileid>")
def fetch(fileid):
    """Return a JSON object containing base64 encoded versions of original and compliant image of fileid hash"""

    compliant_filename = get_filename_from_hash(fileid, "png")
    compliant_path = os.path.join(
        app.config["UPLOAD_FOLDER"], compliant_filename)
    original_path = check_hash_exists(
        fileid + "_orig", app.config["ALLOWED_EXTENSIONS"], app.config["UPLOAD_FOLDER"])

    if not os.path.exists(compliant_path) or not os.path.exists(original_path):
        return jsonify(status=404)

    return jsonify(status=200, original=convert_to_base64(original_path), compliant=convert_to_base64(compliant_path))


@bp.route("/fetch/img/<string:view>/<string:fileid>")
def compliant_view(view, fileid):
    """Return an original or compliant image from the uploads folder if exists in querystring"""

    if view == "original":

        image_filename = check_hash_exists(
            fileid + "_orig", app.config["ALLOWED_EXTENSIONS"], app.config["UPLOAD_FOLDER"])

        if not image_filename:
            abort(404)

        return send_from_directory(os.path.abspath(app.config["UPLOAD_FOLDER"]), image_filename)

    if view == "compliant":

        image_filename = get_filename_from_hash(fileid, "png")

        if not os.path.exists(os.path.join(app.config["UPLOAD_FOLDER"], image_filename)):
            abort(404)

        return send_from_directory(os.path.abspath(app.config['UPLOAD_FOLDER']), image_filename)

    abort(404)


@bp.route("/upload", methods=['POST'])
def upload():
    """Validate and upload a file uploaded to the server via POST"""

    if 'file' not in request.files:
        return "No file!"

    file = request.files['file']

    if file and allowed_file(file.filename):

        filename = secure_filename(file.filename)

        file_hash = hash_filename(app.config['UPLOAD_FOLDER'])

        original_file_path = file_hash + "_precrop." + get_extension(filename)
        uploaded_file_path = file_hash + "_orig." + get_extension(filename)
        watermarked_file_path = file_hash + ".png"

        file.save(original_file_path)
        file.close()

        HandleImage(original_file_path).save(uploaded_file_path)

        cartoon_file = cartoonify(
            uploaded_file_path, app.config["DATASET_FOLDER"], os.path.join(app.config["MODEL_FOLDER"], "frozen_inference_graph.pb"))

        add_watermark(str(cartoon_file), os.path.join(
            app.root_path, "eu-compliant-watermark.png"), watermarked_file_path)

        cleanup_files([original_file_path, cartoon_file])
        return jsonify(status=200, id=file_hash.split("/")[1])
