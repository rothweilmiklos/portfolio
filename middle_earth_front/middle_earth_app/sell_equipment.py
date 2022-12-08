from .purchase_equipment import get_headers, get_username
from . import requests

MIDDLE_EARTH_INVENTORY_SELL_END_POINT = "http://middleearthinventory:8003/api/inventory/id/"
MIDDLE_EARTH_USERS_ENDPOINT = "http://middleearthauth:8001/api/users/"
MIDDLE_EARTH_USER_UPDATE_ENDPOINT = "http://middleearthauth:8001/api/users/"


def get_inventory_id(request):
    return request.POST["sold_equipment_id"]


def get_end_point_for_id_filtered_inventory(request):
    inventory_id = get_inventory_id(request)
    return MIDDLE_EARTH_INVENTORY_SELL_END_POINT + inventory_id + "/"


def get_end_point_for_username_filtered_user(request):
    username = get_username(request)
    return MIDDLE_EARTH_USERS_ENDPOINT + username + "/"


def get_end_point_for_username_filtered_update_user(request):
    username = get_username(request)
    return MIDDLE_EARTH_USER_UPDATE_ENDPOINT + username + "/"


def get_sold_inventory_from_api(request):
    headers = get_headers(request)
    end_point_for_inventory_id_filtered_inventory = get_end_point_for_id_filtered_inventory(request)
    return requests.send_get_request(end_point=end_point_for_inventory_id_filtered_inventory, headers=headers)


def get_seller_from_api(request):
    end_point_for_user = get_end_point_for_username_filtered_user(request)
    headers = get_headers(request)
    return requests.send_get_request(end_point=end_point_for_user, headers=headers)


def invalid_response_status(inventory_response, seller_response):
    return inventory_response.status_code != 200 or seller_response.status_code != 200


def sell_inventory(request):
    headers = get_headers(request)
    end_point_for_inventory_id_filtered_inventor = get_end_point_for_id_filtered_inventory(request)
    response = requests.send_delete_request(end_point=end_point_for_inventory_id_filtered_inventor, headers=headers)
    return response


def update_seller_credit(request, seller_json, equipment_json):
    end_point_for_update_seller = get_end_point_for_username_filtered_update_user(request)
    headers = get_headers(request)

    credit_for_sold_equipment = equipment_json["item_price"]
    seller_credit = seller_json["credit"]
    seller_updated_credit = credit_for_sold_equipment + seller_credit

    parameters_for_update_credit = {
        "credit": seller_updated_credit
    }

    return requests.send_patch_request(end_point=end_point_for_update_seller,
                                       parameters=parameters_for_update_credit,
                                       headers=headers)
