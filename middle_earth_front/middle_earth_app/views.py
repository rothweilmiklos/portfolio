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
from . import utilities, constants
from .models import AuthenticatedUserCaste
from .utilities import decode_access_token

MIDDLE_EARTH_EQUIPMENTS_END_POINT = constants.MIDDLE_EARTH_EQUIPMENTS_END_POINT
MIDDLE_EARTH_ADD_EQUIPMENTS_END_POINT = constants.MIDDLE_EARTH_ADD_EQUIPMENTS_END_POINT
MIDDLE_EARTH_USERS_ENDPOINT = constants.MIDDLE_EARTH_USERS_ENDPOINT
MIDDLE_EARTH_USER_REGISTER_END_POINT = constants.MIDDLE_EARTH_USER_REGISTER_END_POINT
MIDDLE_EARTH_INVENTORY_END_POINT = constants.MIDDLE_EARTH_INVENTORY_PURCHASE_END_POINT
MIDDLE_EARTH_USER_INVENTORY_END_POINT = constants.MIDDLE_EARTH_USER_INVENTORY_END_POINT
MIDDLE_EARTH_INVENTORY_PURCHASE_END_POINT = constants.MIDDLE_EARTH_INVENTORY_PURCHASE_END_POINT
MIDDLE_EARTH_INVENTORY_SELL_END_POINT = constants.MIDDLE_EARTH_INVENTORY_SELL_END_POINT
AUTH_TOKEN_END_POINT = constants.AUTH_TOKEN_END_POINT
MIDDLE_EARTH_PURCHASED_EQUIPMENT_END_POINT = constants.MIDDLE_EARTH_PURCHASED_EQUIPMENT_END_POINT
MIDDLE_EARTH_USER_UPDATE_ENDPOINT = constants.MIDDLE_EARTH_USER_UPDATE_ENDPOINT


# Create your views here.


def user_can_afford_equipment(user, equipment):
    return int(user["credit"]) >= (equipment["price"])


class HomeView(TemplateView):
    template_name = "middle_earth_app/home.html"


class ShopView(LoginRequiredMixin, View):
    login_url = "login"

    @staticmethod
    def get(request):
        caste = request.user.authenticatedusercaste.caste
        end_point_for_caste_filtered_equipments = MIDDLE_EARTH_EQUIPMENTS_END_POINT + caste + "/"
        equipments_from_equipment_api = utilities.send_get_request(end_point=end_point_for_caste_filtered_equipments)
        items_from_equipment_api_json = equipments_from_equipment_api.json()
        return render(request, "middle_earth_app/items.html", {"items": items_from_equipment_api_json})

    @staticmethod
    def post(request):
        purchased_equipment_id = request.POST.get("purchased_equipment_id")
        end_point_for_equipment = MIDDLE_EARTH_PURCHASED_EQUIPMENT_END_POINT + purchased_equipment_id
        purchased_equipment_get_request = utilities.send_get_request(end_point=end_point_for_equipment)
        purchased_equipment_get_request_json = purchased_equipment_get_request.json()

        user_access_token = request.session.get("access_token")
        headers = {
            "Authorization": f"Bearer {user_access_token}"
        }
        username = request.user.username
        end_point_for_user = MIDDLE_EARTH_USERS_ENDPOINT + username + "/"
        user_get_request = utilities.send_get_request(end_point=end_point_for_user, headers=headers)
        user_get_request_json = user_get_request.json()

        invalid_response_status = 200 > (user_get_request.status_code or
                                         purchased_equipment_get_request) > 300

        if invalid_response_status:
            messages.error(request, "Sorry, you can not purchase this item right now. Please try again later!")
            return redirect("items")

        if not user_can_afford_equipment(user_get_request_json,
                                         purchased_equipment_get_request_json):
            messages.warning(request, "Sorry, you can not afford this item. You can sell your item(s) "
                                      "in order to earn credit")
            return redirect("items")

        parameters_for_purchase = {
            "owner_username": user_get_request_json["username"],
            "item_id": purchased_equipment_get_request_json["id"],
            "item_name": purchased_equipment_get_request_json["name"],
            "item_price": purchased_equipment_get_request_json["price"],
            "item_description": purchased_equipment_get_request_json["description"],
            "item_image_url": purchased_equipment_get_request_json["image_url"],
        }
        purchase_api_response = utilities.send_post_request(end_point=MIDDLE_EARTH_INVENTORY_END_POINT,
                                                            parameters=parameters_for_purchase,
                                                            headers=headers)
        if purchase_api_response.status_code != 201:
            messages.error(request, "Sorry, you can not purchase this item right now. Please try again later!")
            return redirect("items")

        reduced_credit = user_get_request_json["credit"] - purchased_equipment_get_request_json["price"]
        parameters_for_update_credit = {
            "credit": reduced_credit
        }

        end_point_for_update_user = MIDDLE_EARTH_USER_UPDATE_ENDPOINT + username + "/"

        update_user_credit = utilities.send_patch_request(end_point=end_point_for_update_user,
                                                          parameters=parameters_for_update_credit,
                                                          headers=headers)

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
        equipments_from_inventory_api = utilities.send_get_request(end_point=end_point_for_user_filtered_equipments,
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
        user_get_request = utilities.send_get_request(end_point=end_point_for_user, headers=headers)
        user_get_request_json = user_get_request.json()

        item_to_be_sold_get_request = utilities.send_get_request(
            end_point=end_point_for_inventory_id_filtered_inventory,
            headers=headers)
        item_to_be_sold_get_request_json = item_to_be_sold_get_request.json()

        sell_equipment_post_request = utilities.send_delete_request(
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

        update_user_credit = utilities.send_patch_request(end_point=end_point_for_update_user,
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

        register_response = utilities.send_post_request(end_point=MIDDLE_EARTH_USER_REGISTER_END_POINT,
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

        login_response = utilities.send_post_request(end_point=AUTH_TOKEN_END_POINT, parameters=parameters)
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

            add_equipment_response = utilities.send_post_request(end_point=MIDDLE_EARTH_ADD_EQUIPMENTS_END_POINT,
                                                                 parameters=parameters_for_register)

            print(add_equipment_response)

        return redirect("add_equipment")
