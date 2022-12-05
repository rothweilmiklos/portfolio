from django.contrib.auth.models import User
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist

from . import requests
from .decode import decode_access_token
from .forms import EntityLoginForm
from .models import AuthenticatedUserCaste


AUTH_TOKEN_END_POINT = "http://middleearthauth:8001/api/token/"


def get_form(request):
    return EntityLoginForm(request.POST)


def get_parameters_for_login(form):
    parameters = {
        "username": form.cleaned_data["username"],
        "password": form.cleaned_data["password"]
    }
    return parameters


def get_user_auth_tokens(form):
    parameters = get_parameters_for_login(form)
    return requests.send_post_request(end_point=AUTH_TOKEN_END_POINT, parameters=parameters)


def add_error_messages(request, response_json):
    for value in response_json.values():
        messages.add_message(request, messages.ERROR, value)
    return request


def create_user(form):
    new_user = User(username=form.cleaned_data["username"])
    new_user.set_password(form.cleaned_data["password"])
    new_user.save()
    return new_user


def add_caste_to_new_user(request, new_user):
    decoded_access_token = decode_access_token(request.session["access_token"])
    caste = decoded_access_token["caste"]
    user_related_caste_row = AuthenticatedUserCaste.objects.get(user_id=new_user.id)
    user_related_caste_row.caste = caste
    user_related_caste_row.save()


def create_user_in_local_database(request, form):
    try:
        User.objects.get(username=form.cleaned_data["username"])
    except ObjectDoesNotExist:
        user_logging_in = create_user(form)
        add_caste_to_new_user(request, user_logging_in)
