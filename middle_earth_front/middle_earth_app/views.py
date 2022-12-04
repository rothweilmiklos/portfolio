from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views import View
from django.views.generic import TemplateView
from django.views.decorators.http import require_http_methods

from .forms import EntityRegistrationForm, EntityLoginForm, AddEquipmentForm
from .decorators import check_if_user_logged_in
from . import requests, shop_view_post, shop_view_get
from .models import AuthenticatedUserCaste
from .decode import decode_access_token

MIDDLE_EARTH_EQUIPMENTS_END_POINT = "http://middleearthitems:8002/api/items/filter/"
MIDDLE_EARTH_ADD_EQUIPMENTS_END_POINT = "http://middleearthitems:8002/api/equipments/"
MIDDLE_EARTH_USERS_ENDPOINT = "http://middleearthauth:8001/api/users/"
MIDDLE_EARTH_USER_REGISTER_END_POINT = "http://middleearthauth:8001/api/register/"
MIDDLE_EARTH_INVENTORY_END_POINT = "http://middleearthinventory:8003/api/inventory/"
MIDDLE_EARTH_USER_INVENTORY_END_POINT = "http://middleearthinventory:8003/api/inventory/filter/"
MIDDLE_EARTH_INVENTORY_PURCHASE_END_POINT = "http://middleearthinventory:8003/api/inventory/"
MIDDLE_EARTH_INVENTORY_SELL_END_POINT = "http://middleearthinventory:8003/api/inventory/id/"
AUTH_TOKEN_END_POINT = "http://middleearthauth:8001/api/token/"
MIDDLE_EARTH_PURCHASED_EQUIPMENT_END_POINT = "http://middleearthitems:8002/api/items/"
MIDDLE_EARTH_USER_UPDATE_ENDPOINT = "http://middleearthauth:8001/api/users/"


# Create your views here.


# def user_can_afford_equipment(user, equipment):
#     return int(user["credit"]) >= (equipment["price"])


class HomeView(TemplateView):
    template_name = "middle_earth_app/home.html"


class ShopView(LoginRequiredMixin, View):
    login_url = "login"

    @staticmethod
    def get(request):
        equipment_list = shop_view_get.get_equipments_list(request)
        return render(request, "middle_earth_app/items.html", {"items": equipment_list})

    @staticmethod
    def post(request):
        purchased_equipment_get_response = shop_view_post.get_purchased_equipment_from_api(request)
        purchased_equipment_get_response_json = purchased_equipment_get_response.json()

        user_get_response = shop_view_post.get_buyer_user_from_api(request)
        user_get_response_json = user_get_response.json()

        if shop_view_post.invalid_response_status(purchased_equipment_get_response, user_get_response):
            messages.error(request, "Sorry, you can not purchase this item right now. Please try again later!")
            return redirect("items")

        if not shop_view_post.user_can_afford_equipment(user_get_response_json,
                                                        purchased_equipment_get_response_json):
            messages.warning(request, "Sorry, you can not afford this item. You can sell your item(s) "
                                      "in order to earn credit")
            return redirect("items")

        purchase_response = shop_view_post.purchase_equipment(request, user_get_response_json,
                                                              purchased_equipment_get_response_json)

        if purchase_response.status_code != 201:
            messages.error(request, "Sorry, you can not purchase this item right now. Please try again later!")
            return redirect("items")

        shop_view_post.update_user_credit(request, user_get_response_json, purchased_equipment_get_response_json)

        messages.success(request, "You have successfully purchased this equipment!")
        return redirect("items")


class InventoryView(LoginRequiredMixin, View):
    login_url = "login"

    @staticmethod
    def get(request):
        username = request.user.username
        end_point_for_user_filtered_equipments = MIDDLE_EARTH_USER_INVENTORY_END_POINT + username + "/"
        user_access_token = request.session.get("access_token")
        headers = {
            "Authorization": f"Bearer {user_access_token}"
        }
        equipments_from_inventory_api = requests.send_get_request(end_point=end_point_for_user_filtered_equipments,
                                                                  headers=headers)
        items_from_inventory_api_json = equipments_from_inventory_api.json()
        return render(request, "middle_earth_app/inventory.html", {"items": items_from_inventory_api_json})

    @staticmethod
    def post(request):
        inventory_id = request.POST["sold_equipment_id"]
        end_point_for_inventory_id_filtered_inventory = MIDDLE_EARTH_INVENTORY_SELL_END_POINT + inventory_id + "/"
        user_access_token = request.session.get("access_token")
        headers = {
            "Authorization": f"Bearer {user_access_token}"
        }

        username = request.user.username
        end_point_for_user = MIDDLE_EARTH_USERS_ENDPOINT + username + "/"
        user_get_request = requests.send_get_request(end_point=end_point_for_user, headers=headers)
        user_get_request_json = user_get_request.json()

        item_to_be_sold_get_request = requests.send_get_request(
            end_point=end_point_for_inventory_id_filtered_inventory,
            headers=headers)
        item_to_be_sold_get_request_json = item_to_be_sold_get_request.json()

        sell_equipment_post_request = requests.send_delete_request(
            end_point=end_point_for_inventory_id_filtered_inventory,
            headers=headers)

        if sell_equipment_post_request.status_code != 204:
            messages.error(request, "Sorry, you can not sell this item right now. Please try again later!")
            return redirect("inventory")

        credit_for_sold_item = item_to_be_sold_get_request_json["item_price"]
        user_credit = user_get_request_json["credit"]

        user_updated_credit = user_credit + credit_for_sold_item

        parameters_for_update_credit = {
            "credit": user_updated_credit
        }

        end_point_for_update_user = MIDDLE_EARTH_USER_UPDATE_ENDPOINT + username + "/"

        update_user_credit = requests.send_patch_request(end_point=end_point_for_update_user,
                                                         parameters=parameters_for_update_credit,
                                                         headers=headers)

        messages.success(request, "You have successfully sold this equipment!")

        return redirect("inventory")


@require_http_methods(["GET", "POST"])
@check_if_user_logged_in
def register_new_user(request):
    if request.method == "POST":
        form = EntityRegistrationForm(request.POST)

        if not form.is_valid():
            messages.error(request, form.errors)
            return redirect("register")

        parameters_for_register = {
            "username": form.cleaned_data["username"],
            "password": form.cleaned_data["password"],
            "password2": form.cleaned_data["password2"],
            "caste": form.cleaned_data["caste"]
        }

        register_response = requests.send_post_request(end_point=MIDDLE_EARTH_USER_REGISTER_END_POINT,
                                                       parameters=parameters_for_register)

        register_response_json = register_response.json()

        if 400 <= register_response.status_code < 500:

            for key, value in register_response_json.items():
                form.add_error(field=key, error=value)

            messages.error(request, message=form.errors)
            return redirect("register")

        elif register_response.status_code == 500:
            messages.info(request, message="Sorry, something went wrong, please try again later!")
            return redirect("register")

        messages.success(request, "Your account has been created successfully!")

        return redirect("login")

    form = EntityRegistrationForm()
    return render(request, "middle_earth_app/register.html", {"form": form})


@require_http_methods(["GET", "POST"])
@check_if_user_logged_in
def login_user(request):
    if request.user.is_authenticated:
        return redirect("items")

    if request.method == "POST":
        form = EntityLoginForm(request.POST)

        if not form.is_valid():
            messages.error(request, "The credentials you've given are not correct, please try again!")
            return redirect("login")

        parameters = {
            "username": form.cleaned_data["username"],
            "password": form.cleaned_data["password"]
        }

        login_response = requests.send_post_request(end_point=AUTH_TOKEN_END_POINT, parameters=parameters)
        login_response_json = login_response.json()

        if 400 <= login_response.status_code < 500:
            message = list(login_response_json.values())
            messages.error(request, message=message[0])
            return redirect("login")

        elif login_response.status_code == 500:
            messages.info(request, message="Sorry, something went wrong, please try again later!")
            return redirect("login")

        request.session["access_token"] = login_response_json["access"].strip()
        request.session["refresh_token"] = login_response_json["refresh"].strip()
        messages.success(request, "You've logged in successfully!")

        try:
            User.objects.get(username=form.cleaned_data["username"])
        except ObjectDoesNotExist:
            user_logging_in = User(username=form.cleaned_data["username"])
            user_logging_in.set_password(form.cleaned_data["password"])
            user_logging_in.save()

            decoded_access_token = decode_access_token(request.session["access_token"])
            caste = decoded_access_token["caste"]
            user_related_caste_row = AuthenticatedUserCaste.objects.get(user_id=user_logging_in.id)
            user_related_caste_row.caste = caste
            user_related_caste_row.save()

        user = authenticate(username=form.cleaned_data["username"], password=form.cleaned_data["password"])

        if user is not None:
            login(request, user)
        return redirect("items")

    form = EntityRegistrationForm()
    return render(request, "middle_earth_app/login.html", {"form": form})


@login_required(login_url="login")
def logout_user(request):
    session_username_value = request.user.username
    try:
        user = User.objects.filter(username=session_username_value)
    except ObjectDoesNotExist:
        return redirect("home")

    logout(request)
    user.delete()
    messages.success(request, "You've logged out successfully!")
    return redirect("home")


class AddEquipmentsView(View):

    @staticmethod
    @staff_member_required(login_url="login")
    def get(request):
        form = AddEquipmentForm()
        return render(request, "middle_earth_app/add_items.html", {"form": form})

    @staticmethod
    @staff_member_required(login_url="login")
    def post(request):
        form = AddEquipmentForm(request.POST)
        if form.is_valid():
            parameters_for_register = {
                "name": form.cleaned_data["name"],
                "price": form.cleaned_data["price"],
                "description": form.cleaned_data["description"],
                "wielder_caste": form.cleaned_data["wielder_caste"],
                "image_url": form.cleaned_data["image_url"],
            }

            add_equipment_response = requests.send_post_request(end_point=MIDDLE_EARTH_ADD_EQUIPMENTS_END_POINT,
                                                                parameters=parameters_for_register)

        return redirect("add_equipment")
