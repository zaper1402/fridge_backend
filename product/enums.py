from django.db import models

# enum class Categories(val value: String) {
#     FRUITS("Fruits"),
#     VEGETABLES("Vegetables"),
#     BAKERY("Bakery"),
#     OIL("Oil"),
#     CANNED_FOOD("Canned Food"),
#     SAUCES("Sauces"),
#     CEREAL("Cereal"),
#     CONDIMENTS("Condiments"),
#     DAIRY("Dairy"),
#     DRINK("Drink"),
#     DRY_GOODS("Dry Goods"),
#     FROZEN_FOOD("Frozen Food"),
#     MEAT("Meat"),
#     PASTA("Pasta"),
#     DRY_FRUITS("Dry Fruits"),
#     SNACKS("Snacks"),
#     SPICES("Spices"),
#     HERBS("Herbs"),
#     READY_TO_EAT_MEALS("Ready-to-eat Meals"),
#     SEAFOOD("Seafood"),
#     DESSERTS("Desserts"),
#     PICKLED_ITEMS("Pickled Items"),
#     NON_ALCOHOLIC_DRINKS("Non-alcoholic Drinks"),
#     BAKING_INGREDIENTS("Baking Ingredients"),
#     OTHER("Other")

# }

class Categories(models.TextChoices):
    FRUIT = 'Fruit'
    VEGETABLE = 'Vegetable'
    BAKERY =  'Bakery'
    OIL = 'Oil'
    CANNED_FOOD = 'Canned Food'
    SAUCES = 'Sauces'
    CEREAL = 'Cereal'
    CONDIMENT = 'Condiment'
    DAIRY = 'Dairy'
    DRINK = 'Drink'
    DRY_GOODS = 'Dry Goods'
    FROZEN_FOOD = 'Frozen Food'
    MEAT = 'Meat'
    PASTA = 'Pasta'
    DRY_FRUITS = 'Dry Fruits'
    SNACKS = 'Snacks'
    SPICES = 'Spices'
    HERBS = 'Herbs'
    READY_TO_EAT_MEALS = 'Ready-to-eat Meals'
    SEAFOOD = 'Seafood'
    DESSERTS = 'Desserts'
    PICKLED_ITEMS = 'Pickled Items'
    NON_ALCOHOLIC_DRINKS = 'Non-alcoholic Drinks'
    BAKING_INGREDIENTS = 'Baking Ingredients'
    OTHER = 'Other'
    



class QuantityType(models.TextChoices):
        KG = 'KG', 'Kilogram'
        GRAM = 'GRAM', 'Gram'
        LITRE = 'LITRE', 'Litre'
        ML = 'ML', 'Millilitre'
        PIECE = 'PIECE', 'Piece'