from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views import View
from django.views.generic import TemplateView

from . import requests, purchase_equipment, equipment_shop, sell_equipment, inventory_equipment, \
    user_register, user_login
from .decorators import deny_if_user_logged_in
from .forms import EntityRegistrationForm, EntityLoginForm, AddEquipmentForm


MIDDLE_EARTH_ADD_EQUIPMENTS_END_POINT = "http://middleearthitems:8002/api/equipments/"


# Create your views here.


class HomeView(TemplateView):
    template_name = "middle_earth_app/home.html"


class ShopView(LoginRequiredMixin, View):
    login_url = "login"

    @staticmethod
    def get(request):
        equipment_list = equipment_shop.get_equipments_list(request)
        user_credit = equipment_shop.get_users_credit(request)
        return render(request, "middle_earth_app/items.html", {"items": equipment_list, "user_credit": user_credit})

    @staticmethod
    def post(request):
        purchased_equipment_get_response = purchase_equipment.get_purchased_equipment_from_api(request)
        purchased_equipment_get_response_json = purchased_equipment_get_response.json()

        user_get_response = purchase_equipment.get_buyer_user_from_api(request)
        user_get_response_json = user_get_response.json()

        if purchase_equipment.invalid_response_status(purchased_equipment_get_response, user_get_response):
            messages.error(request, "Sorry, you can not purchase this item right now. Please try again later!")
            return redirect("items")

        if not purchase_equipment.user_can_afford_equipment(user_get_response_json,
                                                        purchased_equipment_get_response_json):
            messages.warning(request, "Sorry, you can not afford this item. You can sell your item(s) "
                                      "in order to earn credit")
            return redirect("items")

        purchase_response = purchase_equipment.purchase_equipment(request, user_get_response_json,
                                                              purchased_equipment_get_response_json)

        if purchase_response.status_code != 201:
            messages.error(request, "Sorry, you can not purchase this item right now. Please try again later!")
            return redirect("items")

        purchase_equipment.update_user_credit(request, user_get_response_json, purchased_equipment_get_response_json)

        messages.success(request, "You have successfully purchased this equipment!")
        return redirect("items")


class InventoryView(LoginRequiredMixin, View):
    login_url = "login"

    @staticmethod
    def get(request):
        user_inventory = inventory_equipment.get_user_inventory(request)
        return render(request, "middle_earth_app/inventory.html", {"items": user_inventory})

    @staticmethod
    def post(request):
        inventory_get_response_json = sell_equipment.get_sold_inventory_from_api(request)
        seller_get_response_json = sell_equipment.get_seller_from_api(request)

        if sell_equipment.sell_inventory(request).status_code != 204:
            messages.error(request, "Sorry, you can not sell this item right now. Please try again later!")
            return redirect("inventory")

        sell_equipment.update_seller_credit(request, seller_get_response_json, inventory_get_response_json)

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
        form = user_register.get_form(request)

        if not form.is_valid():
            messages.error(request, form.errors)
            return redirect("register")

        register_response = user_register.register(form)
        register_response_json = register_response.json()

        if register_response.status_code != 201:
            error_extended_form = user_register.add_error_messages_to_form(register_response_json, form)
            messages.error(request, message=error_extended_form.errors)
            return redirect("register")

        messages.success(request, "Your account has been created successfully!")

        return redirect("login")


class LogInView(View):

    @staticmethod
    @deny_if_user_logged_in
    def get(request):
        form = EntityLoginForm()
        return render(request, "middle_earth_app/login.html", {"form": form})

    @staticmethod
    @deny_if_user_logged_in
    def post(request):
        form = user_login.get_form(request)
        if not form.is_valid():
            messages.error(request, "The credentials you've given are not correct, please try again!")
            return redirect("login")

        get_token_response = user_login.get_user_auth_tokens(form)
        get_token_response_json = get_token_response.json()

        if get_token_response.status_code != 200:
            user_login.add_error_messages(request, get_token_response_json)
            return redirect("login")

        request.session["access_token"] = get_token_response_json["access"].strip()
        request.session["refresh_token"] = get_token_response_json["refresh"].strip()

        user_login.create_user_in_local_database(request, form)
        user = authenticate(username=form.cleaned_data["username"], password=form.cleaned_data["password"])
        login(request, user)

        messages.success(request, "You've logged in successfully!")
        return redirect("items")


class LogOutView(LoginRequiredMixin, View):
    login_url = "login"

    @staticmethod
    def get(request):
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

            requests.send_post_request(end_point=MIDDLE_EARTH_ADD_EQUIPMENTS_END_POINT,
                                       parameters=parameters_for_register)

        return redirect("add_equipment")
