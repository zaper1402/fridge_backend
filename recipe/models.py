from django.db import models
from .enums import CuisineType, MealType
from django.contrib.postgres.fields import ArrayField

class Recipe(models.Model):
    #TODO