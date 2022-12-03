from django.db import models


# Create your models here.


CASTE_CHOICES = [('WIZARD', 'Wizard'), ('ELF', 'Elf'), ('HUMAN', 'Human'), ('DWARF', 'Dwarf')]


class Equipments(models.Model):
    name = models.CharField(max_length=128)
    price = models.IntegerField()
    description = models.CharField(max_length=1024)
    wielder_caste = models.CharField(max_length=6, choices=CASTE_CHOICES)
    image_url = models.CharField(max_length=1024)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.name

