from django.db import models

#Tokens used to querry for correct recipes
class CuisineType(models.TextChoices):
    ITALIAN = 'ITALIAN', 'Italian'
    MEXICAN = 'MEXICAN', 'Mexican'
    MEDITERRAINIAN = 'MEDITERRANIAN', 'Mediterrainian'
    INDIAN = 'INDIAN', 'Indian'
    FRENCH = 'FRENCH', 'French'
    CHINESE = 'CHINESE', 'Chinese'
    SEAFOOD = 'SEAFOOD', 'Seafood'

class MealType(models.TextChoices):
    BREAKFAST = 'BREAKFAST', 'Breakfast'
    LUNCH = 'LUNCH', 'Lunch'
    DINNER = 'DINNER', 'Dinner'