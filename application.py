from flask import Flask
from flask import Response

application = Flask(__name__)
application.debug = True


@application.route('/', methods=['GET'])
def hello():
    resp = Response("Foo bar baz")
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


if __name__ == "__main__":
    application.run()
