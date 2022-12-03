from django.views import View
from rest_framework.permissions import IsAuthenticated

from .models import MiddleEarthUser
from .serializers import UserRegisterSerializer, UserUpdateSerializer, MyTokenObtainPairSerializer
from rest_framework import generics
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView


# Create your views here.


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class RegisterView(generics.CreateAPIView):
    queryset = MiddleEarthUser.objects.all()
    serializer_class = UserRegisterSerializer


class SingleUserView(APIView):

    def get(self, request, *args, **kwargs):
        view = SingleUserInformationView.as_view()
        return view(request._request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        view = SingleUserUserUpdateView.as_view()
        return view(request._request, *args, **kwargs)


class SingleUserInformationView(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = MiddleEarthUser.objects.all()
    serializer_class = UserRegisterSerializer
    lookup_field = "username"
    lookup_url_kwarg = "user"


class SingleUserUserUpdateView(generics.UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = MiddleEarthUser.objects.all()
    lookup_field = "username"
    lookup_url_kwarg = "user"
    serializer_class = UserUpdateSerializer

    def partial_update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

