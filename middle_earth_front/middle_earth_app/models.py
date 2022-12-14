from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.


class AuthenticatedUserCaste(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    caste = models.CharField(max_length=6)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            AuthenticatedUserCaste.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.authenticatedusercaste.save()