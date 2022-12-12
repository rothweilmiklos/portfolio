

MIDDLE_EARTH_EQUIPMENTS_END_POINT = "http://middleearthitems:8002/api/items/filter/"
MIDDLE_EARTH_USERS_ENDPOINT = "http://middleearthauth:8001/api/users/"


class UserEndPoint:
    def __init__(self, request):
        self.request = request
        self.base_endpoint = MIDDLE_EARTH_USERS_ENDPOINT
        self.end_point = None
        self.get_end_point()

    def get_end_point(self):
        user = self.request.user.username
        self.end_point = self.base_endpoint + user


class CasteFilteredEquipmentEndPoint:
    def __init__(self, request):
        self.request = request
        self.base_endpoint = MIDDLE_EARTH_EQUIPMENTS_END_POINT
        self.end_point = None
        self.get_endpoint()

    def get_endpoint(self):
        caste = self.request.user.authenticatedusercaste.caste
        self.end_point = self.base_endpoint + caste


class PurchasedEquipmentEndPoint:
    def __init__(self, request, base_end_point):
        self.request = request
        self.base_endpoint = base_end_point
        self.end_point = None
        self.get_endpoint()

    def get_endpoint(self):
        purchased_equipment_id = self.request.POST.get("purchased_equipment_id")
        self.end_point = self.base_endpoint + purchased_equipment_id