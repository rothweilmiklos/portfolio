from rest_framework import serializers
from .models import Equipments


class ItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipments
        fields = ["id", "name", "price", "description", "wielder_caste", "image_url"]
