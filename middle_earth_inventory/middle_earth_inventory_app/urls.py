from django.urls import path
from .views import InventoryListView, InventoryPurchaseView, InventorySellView


urlpatterns = [
    path('inventory/filter/<str:username>/', InventoryListView.as_view(), name='inventory_list'),
    path('inventory/', InventoryPurchaseView.as_view(), name='inventory_purchase'),
    path('inventory/id/<int:pk>/', InventorySellView.as_view(), name='inventory_sell'),
]