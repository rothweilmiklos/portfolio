import functools
from django.http import HttpResponseBadRequest


def is_x_requested_with_xml(view_object):
    view_object_request_header_x_requested_with_xml = view_object.request.headers.get('X-Requested-With')
    return view_object_request_header_x_requested_with_xml == "XMLHttpRequest"


def ajax_request(view_func):
    @functools.wraps(view_func)
    def wrapper(*args, **kwargs):
        view_object = args[0]

        if is_x_requested_with_xml(view_object):
            return view_func(*args, **kwargs)

        return HttpResponseBadRequest("Can't Process this Request")

    return wrapper
