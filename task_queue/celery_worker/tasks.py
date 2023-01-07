from celery import Celery
from get_request import GetRequest, ValidateRequest


app = Celery("celeryworker", broker="rabbitmq", backend="redis://redis:6379/0")


@app.task(name="request")
def get_api_response(end_point, parameters=None, headers=None):
    validate = ValidateRequest()
    response = GetRequest(end_point=end_point, validate=validate, parameters=parameters, headers=headers)
    response.get_api_response()
    return response.response