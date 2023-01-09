import unittest
import requests
import responses
from get_request import GetRequest, ValidateRequest


END_POINT = "https://some-end-point.com/random"
HEADERS = {
    "X-Api-Key": "some-key"
}
PARAMETERS = {
    "first": "second"
}


class TestValidateRequest(unittest.TestCase):

    def setUp(self) -> None:
        self.response = requests.Response()

    def test_valid_response(self):
        self.response.status_code = 200
        validate = ValidateRequest()
        validate.validate_response(self.response)

        self.assertFalse(validate.error)
        self.assertFalse(validate.error_message)

    def test_invalid_response(self):
        self.response.status_code = 400
        validate = ValidateRequest()
        validate.validate_response(self.response)

        self.assertTrue(validate.error)
        self.assertTrue(validate.error_message["error"])


class TestGetRequest(unittest.TestCase):

    @responses.activate
    def test_successful_get_request(self):
        responses.get(END_POINT, json={"data": "success"}, status=200)
        request = GetRequest(end_point=END_POINT, validate=ValidateRequest(), parameters=None, headers=None)
        request.get_api_response()

        self.assertEqual(request.response["data"], "success")

    @responses.activate
    def test_successful_get_request_with_headers(self):
        responses.get(END_POINT,
                      match=[responses.matchers.header_matcher({"X-Api-Key": "some-key"})],
                      json={"data": "success"},
                      status=200)
        self.request = GetRequest(end_point=END_POINT, validate=ValidateRequest(), headers=HEADERS, parameters=None)
        self.request.get_api_response()

        self.assertEqual(self.request.response["data"], "success")

    @responses.activate
    def test_successful_get_request_with_parameters(self):
        responses.get(END_POINT,
                      match=[responses.matchers.query_param_matcher({"first": "second"})],
                      json={"data": "success"},
                      status=200)
        request = GetRequest(end_point=END_POINT, validate=ValidateRequest(), headers=None, parameters=PARAMETERS)
        request.get_api_response()

        self.assertEqual(request.response["data"], "success")

    @responses.activate
    def test_unsuccessful_request_get_request(self):
        responses.get(END_POINT, status=400)
        request = GetRequest(END_POINT, validate=ValidateRequest(), headers=None, parameters=None)
        request.get_api_response()

        self.assertTrue(request.validate.error)
        self.assertTrue(request.response["error"])

    @unittest.mock.patch('requests.get')
    def test_request_exception(self, get_mock):
        get_mock.side_effect = requests.exceptions.Timeout()
        request = GetRequest(END_POINT, validate=ValidateRequest(), headers=None, parameters=None)
        request.get_api_response()

        self.assertTrue(request.validate.error)
        self.assertTrue(request.response["error"])
