import requests


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


class ValidateRequest:
    def __init__(self):
        self.error = False
        self.error_message = None
        self.error_handle = ResponseErrorHandle()

    def validate_request(self, response):
        if not response.ok:
            self.error = True
            self.error_message = self.error_handle.handle_error_status_code(response)


class ResponseErrorHandle:
    @staticmethod
    def handle_error_status_code(response):
        if response.status_code >= 500:
            return "You can not do this right now, please try again later!"
        return response.json()


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
        self.validate_response_from_request()

    def send_get_request(self):
        self.get_response = requests.get(url=self.end_point, headers=self.headers)

    def validate_response_from_request(self):
        self.validate.validate_request(self.get_response)
        if not self.validate.error:
            self.response = self.get_response.json()


class PostRequest:
    def __init__(self, request, end_point, parameters, auth=True):
        self.end_point = end_point.end_point
        if auth:
            auth_headers = Headers(request)
            self.headers = auth_headers.headers
        else:
            self.headers = None
        self.parameters = parameters
        self.post_request = None
        self.response = None
        self.validate = ValidateRequest()
        self.send_post_request()
        self.validate_response_from_request()

    def send_post_request(self):
        self.post_request = requests.post(self.end_point, headers=self.headers, json=self.parameters)

    def validate_response_from_request(self):
        self.validate.validate_request(self.post_request)
        if not self.validate.error:
            self.response = self.post_request.json()


class PatchRequest:
    def __init__(self, request, end_point, parameters):
        self.end_point = end_point.end_point
        auth_headers = Headers(request)
        self.headers = auth_headers.headers
        self.parameters = parameters
        self.patch_request = None
        self.response = None
        self.validate = ValidateRequest()
        self.send_patch_request()
        self.validate_response_from_request()

    def send_patch_request(self):
        self.patch_request = requests.patch(self.end_point, headers=self.headers, json=self.parameters)

    def validate_response_from_request(self):
        self.validate.validate_request(self.patch_request)
        if not self.validate.error:
            self.response = self.patch_request.json()


class DeleteRequest:
    def __init__(self, request, end_point):
        self.end_point = end_point.end_point
        auth_headers = Headers(request)
        self.headers = auth_headers.headers
        self.delete_request = None
        self.response = None
        self.validate = ValidateRequest()
        self.send_delete_request()
        self.validate_response_from_request()

    def send_delete_request(self):
        self.delete_request = requests.delete(self.end_point, headers=self.headers)

    def validate_response_from_request(self):
        self.validate.validate_request(self.delete_request)



