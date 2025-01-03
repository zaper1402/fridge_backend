
from django.db.models import TextChoices

class PreferencesTags(TextChoices):
        VEGAN = 'VEGAN', 'Vegan'
        VEGETARIAN = 'VEGETARIAN', 'Vegetarian'
        NON_VEGETARIAN = 'NON_VEGETARIAN', 'Non-Vegetarian',
        GLUTEN_FREE = 'GLUTEN_FREE', 'Gluten Free',
        DAIRY_FREE = 'DAIRY_FREE', 'Dairy Free',
        NONE = 'NONE', 'None'