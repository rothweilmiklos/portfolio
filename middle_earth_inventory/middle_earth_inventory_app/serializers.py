from rest_framework import serializers
from .models import WhoOwnsWhat


class WhoOwnsWhatSerializer(serializers.ModelSerializer):
    class Meta:
        model = WhoOwnsWhat
        fields = ["id", "owner_username", "item_id", "item_name", "item_price", "item_description", "item_image_url"]
