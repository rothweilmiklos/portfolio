from django.urls import path
from .views import HomeView, ShopView, InventoryView, AddEquipmentsView, RegisterView, login_user, LogOutView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('items/', ShopView.as_view(), name='items'),
    path('inventory/', InventoryView.as_view(), name='inventory'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', login_user, name='login'),
    path('logout/', LogOutView.as_view(), name='logout'),
    path('equipments/', AddEquipmentsView.as_view(), name='add_equipment')
]
