from flask import (current_app, Blueprint, request, jsonify)
from utils import Mailchimp

app = current_app
bp = Blueprint("mailchimp", __name__)


def get_ip():
    if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
        return request.environ['REMOTE_ADDR']
    else:
        return request.environ['HTTP_X_FORWARDED_FOR']  # if behind a proxy


@bp.route("/subscribe", methods=['POST'])
def subscribe():
    mc = Mailchimp(app.config["MAILCHIMP_API_KEY"],
                   app.config["MAILCHIMP_LIST"])
    new_user = {
        "email": request.form.get("email"),
        "fname": request.form.get("firstname"),
        "lname": request.form.get("lastname"),
        "country": request.form.get("country"),
        "social": request.form.get("socialmedia"),
        "consent": request.form.get("checked"),
        "ip": get_ip()
    }
    response = mc.subscribe_list_member(new_user)
    return jsonify(status=response["status"])
