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
from .decorators import deny_if_user_logged_in
from . import requests, shop_view_post, shop_view_get, inventory_view_post, inventory_view_get, register_view_post
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
        user_inventory = inventory_view_get.get_user_inventory(request)
        return render(request, "middle_earth_app/inventory.html", {"items": user_inventory})

    @staticmethod
    def post(request):
        inventory_get_response_json = inventory_view_post.get_sold_inventory_from_api(request)
        seller_get_response_json = inventory_view_post.get_seller_from_api(request)

        if inventory_view_post.sell_inventory(request).status_code != 204:
            messages.error(request, "Sorry, you can not sell this item right now. Please try again later!")
            return redirect("inventory")

        inventory_view_post.update_seller_credit(request, seller_get_response_json, inventory_get_response_json)

        messages.success(request, "You have successfully sold this equipment!")
        return redirect("inventory")


class RegisterView(View):

    @staticmethod
    @deny_if_user_logged_in
    def get(request):
        form = EntityRegistrationForm()
        return render(request, "middle_earth_app/register.html", {"form": form})

    @staticmethod
    @deny_if_user_logged_in
    def post(request):
        form = register_view_post.get_form(request)

        if not form.is_valid():
            messages.error(request, form.errors)
            return redirect("register")

        register_response = register_view_post.register(form)
        register_response_json = register_response.json()

        if register_response.status_code != 201:
            error_extended_form = register_view_post.add_error_messages_to_form(register_response_json, form)
            messages.error(request, message=error_extended_form.errors)
            return redirect("register")

        messages.success(request, "Your account has been created successfully!")

        return redirect("login")


@require_http_methods(["GET", "POST"])
@deny_if_user_logged_in
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
