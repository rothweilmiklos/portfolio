import requests
from abc import ABC, abstractmethod


class Validate(ABC):

    @abstractmethod
    def validate_response(self, response):
        pass


class ValidateRequest(Validate):

    def __init__(self):
        self.error = False
        self.error_message = None

    def validate_response(self, response):
        if not response.ok:
            self.error = True
            self.error_message = {"error": True,
                                  "message": "Sorry we could not fetch this data right now. Please try again later"}


class GetRequest:
    def __init__(self, end_point, validate: Validate, parameters, headers):
        self.end_point = end_point
        self.validate = validate
        self.parameters = parameters
        self.headers = headers
        self.get_response = None
        self.response = None
        self.__send_get_request()

    def __send_get_request(self):
        self.get_response = requests.get(url=self.end_point, headers=self.headers, params=self.parameters)

    def get_api_response(self):
        self.validate.validate_response(self.get_response)
        if not self.validate.error:
            self.response = self.get_response.json()
        else:
            self.response = self.validate.error_message
