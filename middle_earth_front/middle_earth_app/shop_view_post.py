from . import requests
from django.contrib import messages
from django.shortcuts import redirect, render

MIDDLE_EARTH_PURCHASED_EQUIPMENT_END_POINT = "http://middleearthitems:8002/api/items/"
MIDDLE_EARTH_USERS_ENDPOINT = "http://middleearthauth:8001/api/users/"
MIDDLE_EARTH_INVENTORY_END_POINT = "http://middleearthinventory:8003/api/inventory/"
MIDDLE_EARTH_USER_UPDATE_ENDPOINT = "http://middleearthauth:8001/api/users/"


def get_headers(request):
    user_access_token = request.session.get("access_token")
    headers = {
        "Authorization": f"Bearer {user_access_token}"
    }
    return headers


def get_username(request):
    return request.user.username


def get_purchased_equipment_from_api(request):
    purchased_equipment_id = request.POST.get("purchased_equipment_id")
    end_point_for_equipment = MIDDLE_EARTH_PURCHASED_EQUIPMENT_END_POINT + purchased_equipment_id
    return requests.send_get_request(end_point=end_point_for_equipment)


def get_buyer_user_from_api(request):
    headers = get_headers(request)
    username = get_username(request)
    end_point_for_user = MIDDLE_EARTH_USERS_ENDPOINT + username + "/"
    return requests.send_get_request(end_point=end_point_for_user, headers=headers)


def invalid_response_status(equipment_response, user_response):
    print(equipment_response.status_code, user_response.status_code)
    return 200 > (equipment_response.status_code or user_response.status_code) >= 300


def user_can_afford_equipment(user, equipment):
    return int(user["credit"]) >= (equipment["price"])


def check_user_can_afford_equipment(request, user_get_response_json, purchased_equipment_get_response_json):
    if not user_can_afford_equipment(user_get_response_json,
                                     purchased_equipment_get_response_json):
        messages.warning(request, "Sorry, you can not afford this item. You can sell your item(s) "
                                  "in order to earn credit")
        return redirect("items")


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


def purchase_equipment(request, user_get_response_json, purchased_equipment_get_response_json):
    parameters_for_purchase = get_parameters_for_purchase(user_get_response_json, purchased_equipment_get_response_json)
    headers_for_purchase = get_headers(request)

    purchase_api_response = requests.send_post_request(end_point=MIDDLE_EARTH_INVENTORY_END_POINT,
                                                       parameters=parameters_for_purchase,
                                                       headers=headers_for_purchase)

    return purchase_api_response


def update_user_credit(request, user_response, equipment_response):
    username = get_username(request)
    end_point_for_update_user = MIDDLE_EARTH_USER_UPDATE_ENDPOINT + username + "/"
    reduced_credit = user_response["credit"] - equipment_response["price"]
    parameters_for_update_credit = {
        "credit": reduced_credit
    }
    headers = get_headers(request)

    requests.send_patch_request(end_point=end_point_for_update_user,
                                parameters=parameters_for_update_credit,
                                headers=headers)


