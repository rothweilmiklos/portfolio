from . import requests
from .shop_view_post import get_buyer_user_from_api


MIDDLE_EARTH_EQUIPMENTS_END_POINT = "http://middleearthitems:8002/api/items/filter/"


def get_equipments_list(request):
    caste = request.user.authenticatedusercaste.caste
    end_point_for_caste_filtered_equipments = MIDDLE_EARTH_EQUIPMENTS_END_POINT + caste + "/"
    get_equipments_response = requests.send_get_request(end_point=end_point_for_caste_filtered_equipments)
    return get_equipments_response.json()


def get_users_credit(request):
    user_response = get_buyer_user_from_api(request)
    if user_response.status_code == 200:
        user_json = user_response.json()
        return user_json["credit"]
