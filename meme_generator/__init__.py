import os

from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from utils.get_dataset import Dataset
from utils.handle_files import hash_filename


APP_ROOT = os.path.join(os.path.dirname(__file__), '..')
dotenv_path = os.path.join(APP_ROOT, '.env')
load_dotenv(dotenv_path)


def create_app(test_config=None):
    """Create and configure the Flask application factory"""

    app = Flask(__name__, instance_relative_config=True)
    CORS(app)
    app.config.from_mapping(
        SECRET_KEY='dev',
        UPLOAD_FOLDER=os.getenv("UPLOAD_FOLDER"),
        MODEL_FOLDER=os.getenv("MODEL_FOLDER"),
        DATASET_FOLDER=os.getenv("DATASET_FOLDER"),
        ALLOWED_EXTENSIONS=set(['png', 'jpg', 'jpeg']),
        MAILCHIMP_API_KEY=os.getenv("MAILCHIMP_API_KEY"),
        MAILCHIMP_LIST=os.getenv("MAILCHIMP_LIST")
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
        os.makedirs(os.path.join(app.instance_path,
                                 app.config['UPLOAD_FOLDER']))
    except OSError:
        pass

    dataset = Dataset(app.config['MODEL_FOLDER'],
                      app.config["DATASET_FOLDER"],
                      app.config["UPLOAD_FOLDER"],
                      os.path.join(app.root_path, "utils/categories.txt"),
                      logging=app.logger)
    dataset.check()

    # register our api blueprints
    from . import api, mailchimp
    app.register_blueprint(api.bp)
    app.register_blueprint(mailchimp.bp)

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    return app
