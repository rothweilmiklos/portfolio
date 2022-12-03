import functools
from django.shortcuts import redirect


def check_if_user_logged_in(view_func):
    @functools.wraps(view_func)
    def wrapper(*args, **kwargs):
        request = args[0]
        if request.user.is_authenticated:
            return redirect("items")

        return view_func(*args, **kwargs)

    return wrapper
