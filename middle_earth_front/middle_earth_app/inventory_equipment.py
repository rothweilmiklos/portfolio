from .purchase_equipment import get_headers, get_username
from . import requests

MIDDLE_EARTH_USER_INVENTORY_END_POINT = "http://middleearthinventory:8003/api/inventory/filter/"


def get_username_filtered_inventory(request):
    username = get_username(request)
    return MIDDLE_EARTH_USER_INVENTORY_END_POINT + username + "/"


def get_user_inventory(request):
    end_point_for_user_filtered_inventory = get_username_filtered_inventory(request)
    headers = get_headers(request)
    response = requests.send_get_request(end_point=end_point_for_user_filtered_inventory, headers=headers)
    if response.status_code == 200:
        return response.json()

