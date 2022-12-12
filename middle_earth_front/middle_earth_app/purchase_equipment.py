from . import requests
from .end_points import UserEndPoint

MIDDLE_EARTH_PURCHASED_EQUIPMENT_END_POINT = "http://middleearthitems:8002/api/items/"
MIDDLE_EARTH_USERS_ENDPOINT = "http://middleearthauth:8001/api/users/"
MIDDLE_EARTH_INVENTORY_END_POINT = "http://middleearthinventory:8003/api/inventory/"
MIDDLE_EARTH_USER_UPDATE_ENDPOINT = "http://middleearthauth:8001/api/users/"


def user_can_afford_equipment(user, equipment):
    return int(user["credit"]) >= (equipment["price"])


def get_parameters_for_purchase(user_get_response_json, purchased_equipment_get_response_json):
    parameters_for_purchase = {
        "owner_username": user_get_response_json["username"],
        "item_id": purchased_equipment_get_response_json["id"],
        "item_name": purchased_equipment_get_response_json["name"],
        "item_price": purchased_equipment_get_response_json["price"],
        "item_description": purchased_equipment_get_response_json["description"],
        "item_image_url": purchased_equipment_get_response_json["image_url"],
    }
    return parameters_for_purchase


def update_user_credit(request, user_response, equipment_response):
    reduced_credit = user_response["credit"] - equipment_response["price"]
    parameters_for_update_credit = {
        "credit": reduced_credit
    }
    requests.PatchRequest(request, end_point=UserEndPoint(request), parameters=parameters_for_update_credit)
