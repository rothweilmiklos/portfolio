from django.urls import path, include
from .views import RegisterView, SingleUserView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register_user'),
    path('users/<user>/', SingleUserView.as_view(), name='user'),
]