import requests
import json



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


class Headers:
    def __init__(self, request):
        self.request = request
        self.headers = None
        self.get_headers()

    def get_headers(self):
        user_access_token = self.request.session.get("access_token")
        if user_access_token is not None:
            self.headers = {
                "Authorization": f"Bearer {user_access_token}"
            }


class GetRequest:
    def __init__(self, request, end_point, auth=False):
        self.end_point = end_point.end_point
        if auth:
            auth_headers = Headers(request)
            self.headers = auth_headers.headers
        else:
            self.headers = None
        self.get_response = None
        self.response = None
        self.validate = ValidateRequest()
        self.send_get_request()
        self.validate_response_from_get_request()

    def send_get_request(self):
        self.get_response = requests.get(url=self.end_point, headers=self.headers)

    def validate_response_from_get_request(self):
        self.validate.validate_get_request(self.get_response)
        if not self.validate.error:
            self.response = self.get_response.json()


class ValidateRequest:
    def __init__(self):
        self.error = False
        self.error_message = None
        self.error_handle = ResponseErrorHandle()

    def validate_get_request(self, response):
        if not response.ok:
            self.error = True
            self.error_message = self.error_handle.handle_error_status_code(response)


class ResponseErrorHandle:
    @staticmethod
    def handle_error_status_code(response):
        if response.status_code >= 500:
            return "You can not do this right now, please try again later!"
        return response.json()
