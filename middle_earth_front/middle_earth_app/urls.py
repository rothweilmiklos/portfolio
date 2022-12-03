from django.urls import path
from .views import HomeView, ShopView, InventoryView, AddEquipmentsView, register_new_user, login_user, logout_user

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('items/', ShopView.as_view(), name='items'),
    path('inventory/', InventoryView.as_view(), name='inventory'),
    path('register/', register_new_user, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('equipments/', AddEquipmentsView.as_view(), name='add_equipment')
]
