import unittest
import requests
import responses
from get_request import GetRequest, ValidateRequest

END_POINT = "https://some-end-point.com/random"

HEADERS = {
    "X-Api-Key": "somekey"
}

PARAMETERS = {
    "first": "second"
}


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
                      match=[responses.matchers.header_matcher({"X-Api-Key": "somekey"})],
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

