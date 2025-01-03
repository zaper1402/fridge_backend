from django.db import models
from django.contrib.postgres.fields import ArrayField
from user.enums import PreferencesTags



class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    age = models.IntegerField()
    preferences = ArrayField(
        models.CharField(max_length=20, choices=PreferencesTags.choices),
        blank=True,
    )
    
