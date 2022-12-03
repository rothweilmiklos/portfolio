from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from .models import MiddleEarthUser
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


def validate_matching_password(password, password2):
    return password == password2


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["caste"] = user.caste
        return token


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = MiddleEarthUser
        fields = ("id", "username", "password", "password2", "caste", "credit")
        extra_kwargs = {
            "caste": {"required": True}
        }

    def validate(self, attrs):
        password = attrs["password"]
        password2 = attrs["password2"]

        if not validate_matching_password(password, password2):
            raise serializers.ValidationError({"password": "Password fields didn't match"})

        return attrs

    def create(self, validated_data):
        user = MiddleEarthUser.objects.create_user(
            username=validated_data["username"],
            caste=validated_data["caste"],
        )

        user.set_password((validated_data["password"]))
        user.save()

        return user


class UserUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = MiddleEarthUser
        fields = ("id", "credit")


