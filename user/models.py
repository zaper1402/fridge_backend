from django.db import models
from django.contrib.postgres.fields import ArrayField
from user.enums import PreferencesTags, GenderChoices



class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=10, choices=GenderChoices.choices, blank=True, null=True)
    photo = models.ImageField(upload_to='photos/', blank=True,null=True)
    preferences = ArrayField(
        models.CharField(max_length=20, choices=PreferencesTags.choices),
        blank=True,
        null=True
    )
    
