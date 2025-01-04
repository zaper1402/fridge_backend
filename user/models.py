from django.db import models
from django.contrib.postgres.fields import ArrayField
from user.enums import PreferencesTags



class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20, blank=True)
    age = models.IntegerField()
    photo = models.ImageField(upload_to='photos/', blank=True,null=True)
    preferences = ArrayField(
        models.CharField(max_length=20, choices=PreferencesTags.choices),
        blank=True,
    )
    
