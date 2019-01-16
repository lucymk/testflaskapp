import json
import requests
from requests.auth import HTTPBasicAuth
from datetime import datetime


class Mailchimp(object):
    def __init__(self, api_key, list_id):
        self.api_key = api_key
        self.datacenter = self.__get_datacenter(api_key)
        self.list_id = list_id

    def __get_datacenter(self, api_key):
        """Determine which datacenter a Mailchimp account is running on"""
        return api_key.split("-")[1]

    def __get_time(self):
        """Create a YYYY-MM-DD HH:MM:SS string from current UTC time"""
        # Mailchimp 3.0 API does not support ISO 8601 input but returns time in this format
        return datetime.utcnow().strftime("%Y-%m-%d %X")

    def subscribe_list_member(self, user):
        """Add a new subscriber to the self.list_id mailing list and return response as JSON"""
        subscribed = "subscribed" if user["consent"] else "unsubscribed"
        payload = {
            "email_address": user["email"],
            "status": subscribed,
            "merge_fields": {
                "FNAME": user["fname"],
                "LNAME": user["lname"],
                "SOCIAL": user["social"]
            },
            "ip_signup": user["ip"],
            "timestamp_signup": self.__get_time(),
            "location": {
                "country_code": user["country"]
            }
        }
        r = requests.post("https://{}.api.mailchimp.com/3.0/lists/{}/members/".format(
            self.datacenter, self.list_id), auth=("anystring", self.api_key), data=json.dumps(payload))
        return r.json()
