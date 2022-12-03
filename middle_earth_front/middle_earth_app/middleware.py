import time
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.core.exceptions import ObjectDoesNotExist

from . import utilities, constants


REFRESH_TOKEN_ENDPOINT = constants.REFRESH_TOKEN_ENDPOINT


def return_response_without_further_modification(request, get_response):
    response = get_response(request)
    return response


def save_new_access_token(request, response):
    request.session["access_token"] = response.json()["access"]


def log_out_user(request):
    logout(request)
    try:
        user = User.objects.filter(username=request.user.username)
    except ObjectDoesNotExist:
        return request
    user.delete()
    return request


def check_valid_new_token(request, response):
    if response.status_code == 200:
        save_new_access_token(request, response)
    else:
        log_out_user(request)
    return request


def try_refresh_token(request, refresh_token):
    parameter = {"refresh": refresh_token}
    refresh_token_response = utilities.send_post_request(end_point=REFRESH_TOKEN_ENDPOINT, parameters=parameter)
    check_valid_new_token(request, refresh_token_response)
    return request


def validate_token_against_expiration(request, payload, refresh_token):
    if payload["exp"] < int(time.time()):
        try_refresh_token(request, refresh_token)
    return request


def refresh_token_middleware(get_response):
    def middleware(request):
        access_token = request.session.get("access_token")
        refresh_token = request.session.get("refresh_token")

        if not request.user.is_authenticated or access_token is None:
            return return_response_without_further_modification(request, get_response)

        access_token_payload = utilities.decode_access_token(access_token)

        request = validate_token_against_expiration(request, access_token_payload, refresh_token)

        return return_response_without_further_modification(request, get_response)

    return middleware
