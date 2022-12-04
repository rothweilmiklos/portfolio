import requests


def send_post_request(end_point, parameters, headers=None):
    response = requests.post(url=end_point, json=parameters, headers=headers)
    return response


def send_delete_request(end_point, headers=None):
    response = requests.delete(url=end_point, headers=headers)
    return response


def send_patch_request(end_point, parameters, headers=None):
    response = requests.patch(url=end_point, json=parameters, headers=headers)
    return response


def send_get_request(end_point, headers=None):
    response = requests.get(url=end_point, headers=headers)
    return response
