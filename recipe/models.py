from django.db import models
from .enums import CuisineType, MealType
from django.contrib.postgres.fields import ArrayField

class Recipe(models.Model):
    name = models.CharField(max_length=100)
    ingredients = ArrayField()
    photo = models.ImageField(upload_to='photos/', blank=True, null=True)
    instructions = models.CharField()
    #TODO