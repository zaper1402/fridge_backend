from django.db import models

class Categories(models.TextChoices):
    DAIRY = 'DAIRY', 'Dairy'
    MEAT_AND_FISH = 'MEAT AND FISH','Meat and Fish'
    VEGETABLE = 'VEGETABLE', 'Vegetable'
    FRUIT = 'FRUIT', 'Fruit'
    GRAIN = 'GRAIN', 'Grain'
    OTHER = 'OTHER', 'Other'


class AllergyTags(models.TextChoices):
    DAIRY = 'DAIRY', 'Dairy'
    NUTS = 'NUTS', 'Nuts'
    GLUTEN = 'GLUTEN', 'Gluten'
    SOY = 'SOY', 'Soy'
    SHELLFISH = 'SHELLFISH', 'Shellfish'
    EGG = 'EGG', 'Egg'
    NONE = 'NONE', 'None'


class QuantityType(models.TextChoices):
        KG = 'KG', 'Kilogram'
        GRAM = 'GRAM', 'Gram'
        LITRE = 'LITRE', 'Litre'
        ML = 'ML', 'Millilitre'
        PIECE = 'PIECE', 'Piece'