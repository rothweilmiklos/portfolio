from . import requests
from middle_earth_app.forms import EntityRegistrationForm


MIDDLE_EARTH_USER_REGISTER_END_POINT = "http://middleearthauth:8001/api/register/"


def get_form(request):
    return EntityRegistrationForm(request.POST)


def get_parameters_for_register(form):
    parameters = {
        "username": form.cleaned_data["username"],
        "password": form.cleaned_data["password"],
        "password2": form.cleaned_data["password2"],
        "caste": form.cleaned_data["caste"]
    }
    return parameters


def add_error_messages_to_form(response_json, form):
    for key, value in response_json.items():
        form.add_error(field=key, error=value)
    return form


