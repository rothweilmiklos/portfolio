import requests
import jwt
from . import constants


PUBLIC_KEY = constants.PUBLIC_KEY


def send_post_request(end_point, parameters, headers=None):
    response = requests.post(url=end_point, json=parameters, headers=headers)
    return response


def send_get_request(end_point, headers=None):
    response = requests.get(url=end_point, headers=headers)
    return response


def send_patch_request(end_point, parameters, headers=None):
    response = requests.patch(url=end_point, json=parameters, headers=headers)
    return response


def send_delete_request(end_point, headers=None):
    response = requests.delete(url=end_point, headers=headers)
    return response


def decode_access_token(access_token):
    decoded_token = jwt.decode(access_token, PUBLIC_KEY, algorithms=["RS256"],
                               options={"verify_signature": False})

    return decoded_token
