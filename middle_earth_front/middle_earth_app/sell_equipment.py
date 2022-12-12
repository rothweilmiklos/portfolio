from .end_points import UserEndPoint
from . import requests


def update_seller_credit(request, seller_json, equipment_json):
    credit_for_sold_equipment = equipment_json["item_price"]
    seller_credit = seller_json["credit"]
    seller_updated_credit = credit_for_sold_equipment + seller_credit
    parameters_for_update_credit = {
        "credit": seller_updated_credit
    }

    requests.PatchRequest(request, end_point=UserEndPoint(request), parameters=parameters_for_update_credit)
