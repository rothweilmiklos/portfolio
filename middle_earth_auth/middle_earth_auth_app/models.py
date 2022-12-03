from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.


CASTE_CHOICES = [('WIZARD', 'Wizard'), ('ELF', 'Elf'), ('HUMAN', 'Human'), ('DWARF', 'Dwarf')]


class MiddleEarthUser(AbstractUser):
    caste = models.CharField(max_length=6, choices=CASTE_CHOICES)
    credit = models.IntegerField(default=1000)

    def __str__(self):
        return self.username
