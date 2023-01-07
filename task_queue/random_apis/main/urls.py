from django.urls import path
from .views import APIView

urlpatterns = [
    path('', APIView.as_view(), name='random_apis'),
]