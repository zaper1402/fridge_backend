from django.db import models

class Categories(models.TextChoices):
    DAIRY = 'DAIRY', 'Dairy'
    MEAT_AND_FISH = 'MEAT_AND_FISH', 'Meat and Fish'
    VEGETABLE = 'VEGETABLE', 'Vegetable'
    FRUIT = 'FRUIT', 'Fruit'
    GRAIN = 'GRAIN', 'Grain'
    OTHER = 'OTHER', 'Other'
    BAKERY = 'BAKERY', 'Bakery'
    OIL = 'OIL', 'Oil'
    CANNED_FOOD = 'CANNED_FOOD', 'Canned Food'
    SAUCES = 'SAUCES', 'Sauces'
    CEREAL = 'CEREAL', 'Cereal'
    CONDIMENT = 'CONDIMENT', 'Condiment'
    DRINK = 'DRINK', 'Drink'
    DRY_GOODS = 'DRY_GOODS', 'Dry Goods'
    FROZEN_FOOD = 'FROZEN_FOOD', 'Frozen Food'
    PASTA = 'PASTA', 'Pasta'
    DRY_FRUITS = 'DRY_FRUITS', 'Dry Fruits'
    SNACKS = 'SNACKS', 'Snacks'
    SPICES = 'SPICES', 'Spices'
    HERBS = 'HERBS', 'Herbs'
    READY_TO_EAT_MEALS = 'READY_TO_EAT_MEALS', 'Ready-to-eat Meals'
    SEAFOOD = 'SEAFOOD', 'Seafood'
    DESSERTS = 'DESSERTS', 'Desserts'
    PICKLED_ITEMS = 'PICKLED_ITEMS', 'Pickled Items'
    BAKING_INGREDIENTS = 'BAKING_INGREDIENTS', 'Baking Ingredients'



class AllergyTags(models.TextChoices):
    APPLE = 'APPLE', 'Apple'
    BANANA = 'BANANA', 'Banana'
    MANGO = 'MANGO', 'Mango'
    CITRUS = 'CITRUS', 'Citrus'
    GRAPE = 'GRAPE', 'Grape'
    PEAR = 'PEAR', 'Pear'
    PINEAPPLE = 'PINEAPPLE', 'Pineapple'
    STRAWBERRY = 'STRAWBERRY', 'Strawberry'
    WATERMELON = 'WATERMELON', 'Watermelon'
    PEACH = 'PEACH', 'Peach'
    PLUM = 'PLUM', 'Plum'
    APRICOT = 'APRICOT', 'Apricot'
    KIWI = 'KIWI', 'Kiwi'
    RASPBERRY = 'RASPBERRY', 'Raspberry'
    BLACKBERRY = 'BLACKBERRY', 'Blackberry'
    CHERRY = 'CHERRY', 'Cherry'
    PAPAYA = 'PAPAYA', 'Papaya'
    GUAVA = 'GUAVA', 'Guava'
    POMEGRANATE = 'POMEGRANATE', 'Pomegranate'
    CANTALOUPE = 'CANTALOUPE', 'Cantaloupe'
    LYCHEE = 'LYCHEE', 'Lychee'
    COCONUT = 'COCONUT', 'Coconut'
    DRAGONFRUIT = 'DRAGONFRUIT', 'Dragonfruit'
    FIG = 'FIG', 'Fig'
    PERSIMMON = 'PERSIMMON', 'Persimmon'
    AVOCADO = 'AVOCADO', 'Avocado'
    MULBERRY = 'MULBERRY', 'Mulberry'
    JACKFRUIT = 'JACKFRUIT', 'Jackfruit'
    SAPODILLA = 'SAPODILLA', 'Sapodilla'
    ELDERBERRY = 'ELDERBERRY', 'Elderberry'
    STARFRUIT = 'STARFRUIT', 'Starfruit'
    LINGONBERRY = 'LINGONBERRY', 'Lingonberry'
    TAMARIND = 'TAMARIND', 'Tamarind'
    GOOSEBERRY = 'GOOSEBERRY', 'Gooseberry'
    SOURSOP = 'SOURSOP', 'Soursop'
    DURIAN = 'DURIAN', 'Durian'
    NANCE = 'NANCE', 'Nance'
    LONGAN = 'LONGAN', 'Longan'
    RAMBUTAN = 'RAMBUTAN', 'Rambutan'
    MARULA = 'MARULA', 'Marula'
    GARLIC = 'GARLIC', 'Garlic'
    POTATO = 'POTATO', 'Potato'
    ONION = 'ONION', 'Onion'
    TOMATO = 'TOMATO', 'Tomato'
    SPINACH = 'SPINACH', 'Spinach'
    CARROT = 'CARROT', 'Carrot'
    BROCCOLI = 'BROCCOLI', 'Broccoli'
    CAULIFLOWER = 'CAULIFLOWER', 'Cauliflower'
    CUCUMBER = 'CUCUMBER', 'Cucumber'
    PEPPER = 'PEPPER', 'Pepper'
    ZUCCHINI = 'ZUCCHINI', 'Zucchini'
    LETTUCE = 'LETTUCE', 'Lettuce'
    EGGPLANT = 'EGGPLANT', 'Eggplant'
    ASPARAGUS = 'ASPARAGUS', 'Asparagus'
    PEA = 'PEA', 'Pea'
    PUMPKIN = 'PUMPKIN', 'Pumpkin'
    SWEET_POTATO = 'SWEET_POTATO', 'Sweet Potato'
    ARTICHOKE = 'ARTICHOKE', 'Artichoke'
    KALE = 'KALE', 'Kale'
    CELERY = 'CELERY', 'Celery'
    LEEK = 'LEEK', 'Leek'
    RADISH = 'RADISH', 'Radish'
    BEETROOT = 'BEETROOT', 'Beetroot'
    TURNIP = 'TURNIP', 'Turnip'
    FENNEL = 'FENNEL', 'Fennel'
    SQUASH = 'SQUASH', 'Squash'
    OKRA = 'OKRA', 'Okra'
    CHARD = 'CHARD', 'Chard'
    CHIVE = 'CHIVE', 'Chive'
    KOHLRABI = 'KOHLRABI', 'Kohlrabi'
    SHALLOT = 'SHALLOT', 'Shallot'
    GINGER = 'GINGER', 'Ginger'
    TARO = 'TARO', 'Taro'
    MUSHROOM = 'MUSHROOM', 'Mushroom'
    ARUGULA = 'ARUGULA', 'Arugula'
    DANDELION = 'DANDELION', 'Dandelion'
    WATERCRESS = 'WATERCRESS', 'Watercress'
    ENDIVE = 'ENDIVE', 'Endive'
    RUTABAGA = 'RUTABAGA', 'Rutabaga'
    CASSAVA = 'CASSAVA', 'Cassava'
    CABBAGE = 'CABBAGE', 'Cabbage'
    SNOW_PEA = 'SNOW_PEA', 'Snow Pea'
    SWEET_CORN = 'SWEET_CORN', 'Sweet Corn'
    CELOSIA = 'CELOSIA', 'Celosia'
    WHEAT = 'WHEAT', 'Wheat'
    GLUTEN = 'GLUTEN', 'Gluten'
    DAIRY = 'DAIRY', 'Dairy'
    NUT = 'NUT', 'Nut'
    EGG = 'EGG', 'Egg'
    POPPY_SEED = 'POPPY_SEED', 'Poppy Seed'
    DRIED_FRUIT = 'DRIED_FRUIT', 'Dried Fruit'
    OLIVE_OIL = 'OLIVE_OIL', 'Olive Oil'
    SOY = 'SOY', 'Soy'
    SUNFLOWER = 'SUNFLOWER', 'Sunflower'
    SESAME = 'SESAME', 'Sesame'
    CANOLA = 'CANOLA', 'Canola'
    PEANUT = 'PEANUT', 'Peanut'
    GRAPESEED = 'GRAPESEED', 'Grapeseed'
    WALNUT = 'WALNUT', 'Walnut'
    PALM_OIL = 'PALM_OIL', 'Palm Oil'
    FLAXSEED = 'FLAXSEED', 'Flaxseed'
    HEMP = 'HEMP', 'Hemp'
    CORN = 'CORN', 'Corn'
    MUSTARD = 'MUSTARD', 'Mustard'
    RICE_BRAN = 'RICE_BRAN', 'Rice Bran'
    MACADAMIA = 'MACADAMIA', 'Macadamia'
    SAFFLOWER = 'SAFFLOWER', 'Safflower'
    PECAN = 'PECAN', 'Pecan'
    HAZELNUT = 'HAZELNUT', 'Hazelnut'
    ALMOND = 'ALMOND', 'Almond'
    CAPSAICIN = 'CAPSAICIN', 'Capsaicin'
    BERGAMOT = 'BERGAMOT', 'Bergamot'
    OLIVE = 'OLIVE', 'Olive'
    GREEN_BEAN = 'GREEN_BEAN', 'Green Bean'
    LIMA_BEAN = 'LIMA_BEAN', 'Lima Bean'
    CHICKEN = 'CHICKEN', 'Chicken'
    BEEF = 'BEEF', 'Beef'
    PORK = 'PORK', 'Pork'
    NIGHTSHADE = 'NIGHTSHADE', 'Nightshade'
    NO_KNOWN_ALLERGEN = 'NO_KNOWN_ALLERGEN', 'No Known Allergen'
    MUNG_BEAN = 'MUNG_BEAN', 'Mung Bean'
    CHILI = 'CHILI', 'Chili'
    HONEY = 'HONEY', 'Honey'
    JAM = 'JAM', 'Jam'
    BALSAMIC = 'BALSAMIC', 'Balsamic'
    MAPLE = 'MAPLE', 'Maple'
    AGAVE = 'AGAVE', 'Agave'
    LACTOSE_INTOLERANCE = 'LACTOSE_INTOLERANCE', 'Lactose Intolerance'
    TREE_NUT = 'TREE_NUT', 'Tree Nut'
    HIGH_SUGAR = 'HIGH_SUGAR', 'High Sugar'
    CAFFEINE = 'CAFFEINE', 'Caffeine'
    SUGAR = 'SUGAR', 'Sugar'
    ALCOHOL = 'ALCOHOL', 'Alcohol'
    SHELLFISH = 'SHELLFISH', 'Shellfish'
    MEAT = 'MEAT', 'Meat'
    LEGUME = 'LEGUME', 'Legume'
    OATS = 'OATS', 'Oats'
    GELATIN = 'GELATIN', 'Gelatin'
    FISH = 'FISH', 'Fish'


class QuantityType(models.TextChoices):
        KG = 'KG', 'Kilogram'
        GRAM = 'GRAM', 'Gram'
        LITRE = 'LITRE', 'Litre'
        ML = 'ML', 'Millilitre'
        PIECE = 'PIECE', 'Piece'



CATEGORIES = [
    {"id": "DAIRY", "name": "Dairy"},
    {"id": "MEAT_AND_FISH", "name": "Meat and Fish"},
    {"id": "VEGETABLE", "name": "Vegetable"},
    {"id": "FRUIT", "name": "Fruit"},
    {"id": "GRAIN", "name": "Grain"},
    {"id": "OTHER", "name": "Other"},
    {"id": "BAKERY", "name": "Bakery"},
    {"id": "OIL", "name": "Oil"},
    {"id": "CANNED_FOOD", "name": "Canned Food"},
    {"id": "SAUCES", "name": "Sauces"},
    {"id": "CEREAL", "name": "Cereal"},
    {"id": "CONDIMENT", "name": "Condiment"},
    {"id": "DRINK", "name": "Drink"},
    {"id": "DRY_GOODS", "name": "Dry Goods"},
    {"id": "FROZEN_FOOD", "name": "Frozen Food"},
    {"id": "PASTA", "name": "Pasta"},
    {"id": "DRY_FRUITS", "name": "Dry Fruits"},
    {"id": "SNACKS", "name": "Snacks"},
    {"id": "SPICES", "name": "Spices"},
    {"id": "HERBS", "name": "Herbs"},
    {"id": "READY_TO_EAT_MEALS", "name": "Ready-to-eat Meals"},
    {"id": "SEAFOOD", "name": "Seafood"},
    {"id": "DESSERTS", "name": "Desserts"},
    {"id": "PICKLED_ITEMS", "name": "Pickled Items"},
    {"id": "BAKING_INGREDIENTS", "name": "Baking Ingredients"},
]

ALLERGY_TAGS = [
    {"id": "APPLE", "name": "Apple"},
    {"id": "BANANA", "name": "Banana"},
    {"id": "MANGO", "name": "Mango"},
    {"id": "CITRUS", "name": "Citrus"},
    {"id": "GRAPE", "name": "Grape"},
    {"id": "PEAR", "name": "Pear"},
    {"id": "PINEAPPLE", "name": "Pineapple"},
    {"id": "STRAWBERRY", "name": "Strawberry"},
    {"id": "WATERMELON", "name": "Watermelon"},
    {"id": "PEACH", "name": "Peach"},
    {"id": "PLUM", "name": "Plum"},
    {"id": "APRICOT", "name": "Apricot"},
    {"id": "KIWI", "name": "Kiwi"},
    {"id": "RASPBERRY", "name": "Raspberry"},
    {"id": "BLACKBERRY", "name": "Blackberry"},
    {"id": "CHERRY", "name": "Cherry"},
    {"id": "PAPAYA", "name": "Papaya"},
    {"id": "GUAVA", "name": "Guava"},
    {"id": "POMEGRANATE", "name": "Pomegranate"},
    {"id": "CANTALOUPE", "name": "Cantaloupe"},
    {"id": "LYCHEE", "name": "Lychee"},
    {"id": "COCONUT", "name": "Coconut"},
    {"id": "DRAGONFRUIT", "name": "Dragonfruit"},
    {"id": "FIG", "name": "Fig"},
    {"id": "PERSIMMON", "name": "Persimmon"},
    {"id": "AVOCADO", "name": "Avocado"},
    {"id": "MULBERRY", "name": "Mulberry"},
    {"id": "JACKFRUIT", "name": "Jackfruit"},
    {"id": "SAPODILLA", "name": "Sapodilla"},
    {"id": "ELDERBERRY", "name": "Elderberry"},
    {"id": "STARFRUIT", "name": "Starfruit"},
    {"id": "LINGONBERRY", "name": "Lingonberry"},
    {"id": "TAMARIND", "name": "Tamarind"},
    {"id": "GOOSEBERRY", "name": "Gooseberry"},
    {"id": "SOURSOP", "name": "Soursop"},
    {"id": "DURIAN", "name": "Durian"},
    {"id": "NANCE", "name": "Nance"},
    {"id": "LONGAN", "name": "Longan"},
    {"id": "RAMBUTAN", "name": "Rambutan"},
    {"id": "MARULA", "name": "Marula"},
    {"id": "GARLIC", "name": "Garlic"},
    {"id": "POTATO", "name": "Potato"},
    {"id": "ONION", "name": "Onion"},
    {"id": "TOMATO", "name": "Tomato"},
    {"id": "SPINACH", "name": "Spinach"},
    {"id": "CARROT", "name": "Carrot"},
    {"id": "BROCCOLI", "name": "Broccoli"},
    {"id": "CAULIFLOWER", "name": "Cauliflower"},
    {"id": "CUCUMBER", "name": "Cucumber"},
    {"id": "PEPPER", "name": "Pepper"},
    {"id": "ZUCCHINI", "name": "Zucchini"},
    {"id": "LETTUCE", "name": "Lettuce"},
    {"id": "EGGPLANT", "name": "Eggplant"},
    {"id": "PEANUT", "name": "Peanut"},
    {"id": "NUT", "name": "Nut"},
    {"id": "DAIRY", "name": "Dairy"},
    {"id": "EGG", "name": "Egg"},
    {"id": "SOY", "name": "Soy"},
    {"id": "WHEAT", "name": "Wheat"},
    {"id": "GLUTEN", "name": "Gluten"},
    {"id": "SHELLFISH", "name": "Shellfish"},
    {"id": "FISH", "name": "Fish"},
    {"id": "MEAT", "name": "Meat"},
    {"id": "OATS", "name": "Oats"},
    {"id": "GELATIN", "name": "Gelatin"},
    {"id": "HIGH_SUGAR", "name": "High Sugar"},
    {"id": "CAFFEINE", "name": "Caffeine"},
    {"id": "ALCOHOL", "name": "Alcohol"},
]

QUANTITY_TYPES = [
    {"id": "KG", "name": "Kilogram"},
    {"id": "GRAM", "name": "Gram"},
    {"id": "LITRE", "name": "Litre"},
    {"id": "ML", "name": "Millilitre"},
    {"id": "PIECE", "name": "Piece"},
]
