import hashlib

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views import View
from django.views.generic import TemplateView

from . import requests, purchase_equipment, sell_equipment, user_register, user_login
from .decorators import deny_if_user_logged_in
from .forms import EntityRegistrationForm, EntityLoginForm, AddEquipmentForm
from .end_points import UserEndPoint, CasteFilteredEquipmentEndPoint, PurchasedEquipmentEndPoint, \
    PurchaseEquipmentEndPoint, UserFilterInventoryEndPoint, InventoryEndPoint, RegisterEndPoint, TokenEndPoint, \
    AddEquipmentEndPoint


# Create your views here.


class HomeView(TemplateView):
    template_name = "middle_earth_app/home.html"


class ShopView(LoginRequiredMixin, View):
    login_url = "login"

    @staticmethod
    def get(request):
        equipment_list_api = requests.GetRequest(request, end_point=CasteFilteredEquipmentEndPoint(request), auth=False)
        user_api = requests.GetRequest(request, end_point=UserEndPoint(request), auth=True)

        if not (equipment_list_api.validate.error or user_api.validate.error):
            return render(request, "middle_earth_app/items.html", {"items": equipment_list_api.response,
                                                                   "user_credit": user_api.response["credit"]})

        messages.error(request, message=equipment_list_api.validate.error_message or user_api.validate.error_message)
        return render(request, "middle_earth_app/items.html")

    @staticmethod
    def post(request):
        purchased_equipment_api = requests.GetRequest(request, end_point=PurchasedEquipmentEndPoint(request), auth=True)
        if purchased_equipment_api.validate.error:
            messages.error(request, message=purchased_equipment_api.validate.error_message)
            return redirect("items")

        user_api = requests.GetRequest(request, end_point=UserEndPoint(request), auth=True)
        if user_api.validate.error:
            messages.error(request, message=user_api.validate.error_message)
            return redirect("items")

        purchased_equipment_api_json = purchased_equipment_api.response
        user_api_json = user_api.response

        if not purchase_equipment.user_can_afford_equipment(user_api_json,
                                                            purchased_equipment_api_json):
            messages.warning(request, "Sorry, you can not afford this item. You can sell your item(s) "
                                      "in order to earn credit")
            return redirect("items")

        parameters_for_purchase = purchase_equipment.get_parameters_for_purchase(user_api_json,
                                                                                 purchased_equipment_api_json)

        purchase_api = requests.PostRequest(request,
                                            end_point=PurchaseEquipmentEndPoint(),
                                            parameters=parameters_for_purchase)

        if purchase_api.validate.error:
            messages.error(request, message=purchase_api.validate.error_message)
            return redirect("items")

        purchase_equipment.update_user_credit(request, user_api_json, purchased_equipment_api_json)
        messages.success(request, "You have successfully purchased this equipment!")
        return redirect("thank_you", act="purchased", name=purchased_equipment_api_json["name"])


class InventoryView(LoginRequiredMixin, View):
    login_url = "login"

    @staticmethod
    def get(request):
        user_inventory_api = requests.GetRequest(request, end_point=UserFilterInventoryEndPoint(request), auth=True)
        if user_inventory_api.validate.error:
            messages.error(request, message=user_inventory_api.validate.error_message)
        return render(request, "middle_earth_app/inventory.html", {"items": user_inventory_api.response})

    @staticmethod
    def post(request):
        sold_inventory_api = requests.GetRequest(request, end_point=InventoryEndPoint(request), auth=True)
        if sold_inventory_api.validate.error:
            messages.error(request, message=sold_inventory_api.validate.error_message)
            return redirect("inventory")

        seller_api = requests.GetRequest(request, end_point=UserEndPoint(request), auth=True)
        if seller_api.validate.error:
            messages.error(request, message=seller_api.validate.error_message)
            return redirect("inventory")

        sold_inventory_api_json = sold_inventory_api.response
        seller_api_json = seller_api.response

        sell_equipment_api = requests.DeleteRequest(request, InventoryEndPoint(request), )

        if sell_equipment_api.validate.error:
            messages.error(request, "Sorry, you can not sell this item right now. Please try again later!")
            return redirect("inventory")

        sell_equipment.update_seller_credit(request, seller_api_json, sold_inventory_api_json)
        messages.success(request, "You have successfully sold this equipment!")
        return redirect("thank_you", act="sold", name=sold_inventory_api_json["item_name"])


class ThankYouView(LoginRequiredMixin, View):
    login_url = "login"

    @staticmethod
    def get(request, act, name):
        return render(request,
                      template_name="middle_earth_app/thank_you.html",
                      context={"action": act, "item_name": name})


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

        parameters_for_register = user_register.get_parameters_for_register(form)
        register_api = requests.PostRequest(request,
                                            end_point=RegisterEndPoint(),
                                            parameters=parameters_for_register,
                                            auth=False)

        if register_api.validate.error:
            error_extended_form = user_register.add_error_messages_to_form(register_api.validate.error_message, form)
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

        parameters_for_login = user_login.get_parameters_for_login(form)

        token_api = requests.PostRequest(request,
                                         end_point=TokenEndPoint(),
                                         parameters=parameters_for_login,
                                         auth=False)

        if token_api.validate.error:
            user_login.add_error_messages(request, token_api.validate.error_message)
            return redirect("login")

        token_api_json = token_api.response
        request.session["access_token"] = token_api_json["access"].strip()
        request.session["refresh_token"] = token_api_json["refresh"].strip()

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
            }

            requests.PostRequest(request,
                                 end_point=AddEquipmentEndPoint(),
                                 parameters=parameters_for_register,
                                 auth=False)

        return redirect("add_equipment")
