# Generated by Django 4.2 on 2025-02-15 14:17

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='allergy_tags',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(choices=[('APPLE', 'Apple'), ('BANANA', 'Banana'), ('MANGO', 'Mango'), ('CITRUS', 'Citrus'), ('GRAPE', 'Grape'), ('PEAR', 'Pear'), ('PINEAPPLE', 'Pineapple'), ('STRAWBERRY', 'Strawberry'), ('WATERMELON', 'Watermelon'), ('PEACH', 'Peach'), ('PLUM', 'Plum'), ('APRICOT', 'Apricot'), ('KIWI', 'Kiwi'), ('RASPBERRY', 'Raspberry'), ('BLACKBERRY', 'Blackberry'), ('CHERRY', 'Cherry'), ('PAPAYA', 'Papaya'), ('GUAVA', 'Guava'), ('POMEGRANATE', 'Pomegranate'), ('CANTALOUPE', 'Cantaloupe'), ('LYCHEE', 'Lychee'), ('COCONUT', 'Coconut'), ('DRAGONFRUIT', 'Dragonfruit'), ('FIG', 'Fig'), ('PERSIMMON', 'Persimmon'), ('AVOCADO', 'Avocado'), ('MULBERRY', 'Mulberry'), ('JACKFRUIT', 'Jackfruit'), ('SAPODILLA', 'Sapodilla'), ('ELDERBERRY', 'Elderberry'), ('STARFRUIT', 'Starfruit'), ('LINGONBERRY', 'Lingonberry'), ('TAMARIND', 'Tamarind'), ('GOOSEBERRY', 'Gooseberry'), ('SOURSOP', 'Soursop'), ('DURIAN', 'Durian'), ('NANCE', 'Nance'), ('LONGAN', 'Longan'), ('RAMBUTAN', 'Rambutan'), ('MARULA', 'Marula'), ('GARLIC', 'Garlic'), ('POTATO', 'Potato'), ('ONION', 'Onion'), ('TOMATO', 'Tomato'), ('SPINACH', 'Spinach'), ('CARROT', 'Carrot'), ('BROCCOLI', 'Broccoli'), ('CAULIFLOWER', 'Cauliflower'), ('CUCUMBER', 'Cucumber'), ('PEPPER', 'Pepper'), ('ZUCCHINI', 'Zucchini'), ('LETTUCE', 'Lettuce'), ('EGGPLANT', 'Eggplant'), ('ASPARAGUS', 'Asparagus'), ('PEA', 'Pea'), ('PUMPKIN', 'Pumpkin'), ('SWEET_POTATO', 'Sweet Potato'), ('ARTICHOKE', 'Artichoke'), ('KALE', 'Kale'), ('CELERY', 'Celery'), ('LEEK', 'Leek'), ('RADISH', 'Radish'), ('BEETROOT', 'Beetroot'), ('TURNIP', 'Turnip'), ('FENNEL', 'Fennel'), ('SQUASH', 'Squash'), ('OKRA', 'Okra'), ('CHARD', 'Chard'), ('CHIVE', 'Chive'), ('KOHLRABI', 'Kohlrabi'), ('SHALLOT', 'Shallot'), ('GINGER', 'Ginger'), ('TARO', 'Taro'), ('MUSHROOM', 'Mushroom'), ('ARUGULA', 'Arugula'), ('DANDELION', 'Dandelion'), ('WATERCRESS', 'Watercress'), ('ENDIVE', 'Endive'), ('RUTABAGA', 'Rutabaga'), ('CASSAVA', 'Cassava'), ('CABBAGE', 'Cabbage'), ('SNOW_PEA', 'Snow Pea'), ('SWEET_CORN', 'Sweet Corn'), ('CELOSIA', 'Celosia'), ('WHEAT', 'Wheat'), ('GLUTEN', 'Gluten'), ('DAIRY', 'Dairy'), ('NUT', 'Nut'), ('EGG', 'Egg'), ('POPPY_SEED', 'Poppy Seed'), ('DRIED_FRUIT', 'Dried Fruit'), ('OLIVE_OIL', 'Olive Oil'), ('SOY', 'Soy'), ('SUNFLOWER', 'Sunflower'), ('SESAME', 'Sesame'), ('CANOLA', 'Canola'), ('PEANUT', 'Peanut'), ('GRAPESEED', 'Grapeseed'), ('WALNUT', 'Walnut'), ('PALM_OIL', 'Palm Oil'), ('FLAXSEED', 'Flaxseed'), ('HEMP', 'Hemp'), ('CORN', 'Corn'), ('MUSTARD', 'Mustard'), ('RICE_BRAN', 'Rice Bran'), ('MACADAMIA', 'Macadamia'), ('SAFFLOWER', 'Safflower'), ('PECAN', 'Pecan'), ('HAZELNUT', 'Hazelnut'), ('ALMOND', 'Almond'), ('CAPSAICIN', 'Capsaicin'), ('BERGAMOT', 'Bergamot'), ('OLIVE', 'Olive'), ('GREEN_BEAN', 'Green Bean'), ('LIMA_BEAN', 'Lima Bean'), ('CHICKEN', 'Chicken'), ('BEEF', 'Beef'), ('PORK', 'Pork'), ('NIGHTSHADE', 'Nightshade'), ('NO_KNOWN_ALLERGEN', 'No Known Allergen'), ('MUNG_BEAN', 'Mung Bean'), ('CHILI', 'Chili'), ('HONEY', 'Honey'), ('JAM', 'Jam'), ('BALSAMIC', 'Balsamic'), ('MAPLE', 'Maple'), ('AGAVE', 'Agave'), ('LACTOSE_INTOLERANCE', 'Lactose Intolerance'), ('TREE_NUT', 'Tree Nut'), ('HIGH_SUGAR', 'High Sugar'), ('CAFFEINE', 'Caffeine'), ('SUGAR', 'Sugar'), ('ALCOHOL', 'Alcohol'), ('SHELLFISH', 'Shellfish'), ('MEAT', 'Meat'), ('LEGUME', 'Legume'), ('OATS', 'Oats'), ('GELATIN', 'Gelatin'), ('FISH', 'Fish')], max_length=50), blank=True, null=True, size=None),
        ),
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.CharField(choices=[('DAIRY', 'Dairy'), ('MEAT_AND_FISH', 'Meat and Fish'), ('VEGETABLE', 'Vegetable'), ('FRUIT', 'Fruit'), ('GRAIN', 'Grain'), ('OTHER', 'Other'), ('BAKERY', 'Bakery'), ('OIL', 'Oil'), ('CANNED_FOOD', 'Canned Food'), ('SAUCES', 'Sauces'), ('CEREAL', 'Cereal'), ('CONDIMENT', 'Condiment'), ('DRINK', 'Drink'), ('DRY_GOODS', 'Dry Goods'), ('FROZEN_FOOD', 'Frozen Food'), ('PASTA', 'Pasta'), ('DRY_FRUITS', 'Dry Fruits'), ('SNACKS', 'Snacks'), ('SPICES', 'Spices'), ('HERBS', 'Herbs'), ('READY_TO_EAT_MEALS', 'Ready-to-eat Meals'), ('SEAFOOD', 'Seafood'), ('DESSERTS', 'Desserts'), ('PICKLED_ITEMS', 'Pickled Items'), ('BAKING_INGREDIENTS', 'Baking Ingredients')], max_length=20),
        ),
        migrations.AlterField(
            model_name='product',
            name='quantity_type',
            field=models.CharField(choices=[('KG', 'Kilogram'), ('GRAM', 'Gram'), ('LITRE', 'Litre'), ('ML', 'Millilitre'), ('PIECE', 'Piece')], default=0, max_length=50),
        ),
    ]
