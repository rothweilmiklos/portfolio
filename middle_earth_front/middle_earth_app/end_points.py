from abc import ABC, abstractmethod

MIDDLE_EARTH_USERS_ENDPOINT = "http://middleearthauth:8001/api/users/"
MIDDLE_EARTH_EQUIPMENTS_END_POINT = "http://middleearthitems:8002/api/items/filter/"
MIDDLE_EARTH_PURCHASED_EQUIPMENT_END_POINT = "http://middleearthitems:8002/api/items/"
MIDDLE_EARTH_INVENTORY_END_POINT = "http://middleearthinventory:8003/api/inventory/"
MIDDLE_EARTH_INVENTORY_SELL_END_POINT = "http://middleearthinventory:8003/api/inventory/id/"
MIDDLE_EARTH_USER_INVENTORY_END_POINT = "http://middleearthinventory:8003/api/inventory/filter/"
MIDDLE_EARTH_USER_REGISTER_END_POINT = "http://middleearthauth:8001/api/register/"
AUTH_TOKEN_END_POINT = "http://middleearthauth:8001/api/token/"
MIDDLE_EARTH_ADD_EQUIPMENTS_END_POINT = "http://middleearthitems:8002/api/equipments/"
REFRESH_TOKEN_ENDPOINT = "http://middleearthauth:8001/api/token/refresh/"


class EndPoint(ABC):
    @abstractmethod
    def get_end_point(self):
        pass


class UserEndPoint(EndPoint):
    def __init__(self, request):
        self.request = request
        self.base_endpoint = MIDDLE_EARTH_USERS_ENDPOINT
        self.end_point = None
        self.get_end_point()

    def get_end_point(self):
        user = self.request.user.username
        self.end_point = self.base_endpoint + user + "/"


class CasteFilteredEquipmentEndPoint(EndPoint):
    def __init__(self, request):
        self.request = request
        self.base_endpoint = MIDDLE_EARTH_EQUIPMENTS_END_POINT
        self.end_point = None
        self.get_end_point()

    def get_end_point(self):
        caste = self.request.user.authenticatedusercaste.caste
        self.end_point = self.base_endpoint + caste + "/"


class PurchasedEquipmentEndPoint(EndPoint):
    def __init__(self, request):
        self.request = request
        self.base_endpoint = MIDDLE_EARTH_PURCHASED_EQUIPMENT_END_POINT
        self.end_point = None
        self.get_end_point()

    def get_end_point(self):
        purchased_equipment_id = self.request.POST.get("purchased_equipment_id")
        self.end_point = self.base_endpoint + purchased_equipment_id + "/"


class PurchaseEquipmentEndPoint(EndPoint):
    def __init__(self):
        self.base_endpoint = "http://middleearthinventory:8003/api/inventory/"
        self.end_point = None
        self.get_end_point()

    def get_end_point(self):
        self.end_point = self.base_endpoint


class UserFilterInventoryEndPoint(EndPoint):
    def __init__(self, request):
        self.request = request
        self.base_endpoint = MIDDLE_EARTH_USER_INVENTORY_END_POINT
        self.end_point = None
        self.get_end_point()

    def get_end_point(self):
        user = self.request.user.username
        self.end_point = self.base_endpoint + user + "/"


class InventoryEndPoint(EndPoint):
    def __init__(self, request):
        self.request = request
        self.base_endpoint = MIDDLE_EARTH_INVENTORY_SELL_END_POINT
        self.end_point = None
        self.get_end_point()

    def get_end_point(self):
        inventory_id = self.request.POST["sold_equipment_id"]
        self.end_point = self.base_endpoint + inventory_id + "/"


class RegisterEndPoint(EndPoint):
    def __init__(self):
        self.base_endpoint = MIDDLE_EARTH_USER_REGISTER_END_POINT
        self.end_point = None
        self.get_end_point()

    def get_end_point(self):
        self.end_point = self.base_endpoint


class TokenEndPoint(EndPoint):
    def __init__(self):
        self.base_endpoint = AUTH_TOKEN_END_POINT
        self.end_point = None
        self.get_end_point()

    def get_end_point(self):
        self.end_point = self.base_endpoint


class AddEquipmentEndPoint(EndPoint):
    def __init__(self):
        self.base_endpoint = MIDDLE_EARTH_ADD_EQUIPMENTS_END_POINT
        self.end_point = None
        self.get_end_point()

    def get_end_point(self):
        self.end_point = self.base_endpoint


class RefreshTokenEndPoint(EndPoint):
    def __init__(self):
        self.base_endpoint = REFRESH_TOKEN_ENDPOINT
        self.end_point = None
        self.get_end_point()

    def get_end_point(self):
        self.end_point = self.base_endpoint
