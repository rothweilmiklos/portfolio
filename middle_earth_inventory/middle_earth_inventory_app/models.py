from django.db import models


# Create your models here.


class WhoOwnsWhat(models.Model):
    owner_username = models.CharField(max_length=128)
    item_id = models.IntegerField()
    item_name = models.CharField(max_length=128)
    item_price = models.IntegerField()
    item_description = models.CharField(max_length=1024)
    item_image_url = models.CharField(max_length=1024)
