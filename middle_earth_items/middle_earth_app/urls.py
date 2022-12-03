from django.urls import path
from .views import EquipmentsView, PurchasedEquipmentView, AddEquipment

urlpatterns = [
    path('items/filter/<str:wielder_caste>/', EquipmentsView.as_view(), name='items'),
    path('items/<int:id>/', PurchasedEquipmentView.as_view(), name="purchased_item"),
    path('equipments/', AddEquipment.as_view(), name="add_equipment"),
]