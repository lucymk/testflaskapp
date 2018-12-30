from flask import (Flask, Response, request)

application = Flask(__name__)
application.debug = True


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

        print("file", file)

        resp = Response("We got the file.")
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp


if __name__ == "__main__":
    application.run()
