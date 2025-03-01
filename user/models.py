from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.contrib.postgres.fields import ArrayField
from user.enums import PreferencesTags, GenderChoices
from django.contrib.auth.models import AbstractUser
from product.enums import Categories, QuantityType
from product.models import Product
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import password_validation
from django.contrib.auth.hashers import (
    check_password,
    is_password_usable,
    make_password,
)


class User(AbstractUser):
    username = models.CharField(max_length=150,unique=False,null=True, blank=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    date_of_birth = models.DateTimeField(blank=True, null=True)
    gender = models.CharField(max_length=10, choices=GenderChoices.choices, blank=True, null=True)
    photo = models.ImageField(upload_to='photos/', blank=True,null=True)
    preferences = ArrayField(
        models.CharField(max_length=20, choices=PreferencesTags.choices),
        blank=True,
        null=True
    )
    groups = models.ManyToManyField(Group, related_name="custom_user_groups", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="custom_user_permissions", blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS=[]

class UserProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    subname = models.CharField(max_length=100, blank=False, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_product")
    @property
    def total_quantity(self):
        return sum(entry.quantity for entry in self.entry_set.all())

class Entry(models.Model):
    user_inventory = models.ForeignKey(UserProduct, on_delete=models.CASCADE)
    quantity = models.FloatField()
    expiry_date = models.DateTimeField()
    creation_date = models.DateField(auto_now_add=True)  
    quantity_type= models.CharField(max_length=50, choices=QuantityType.choices, blank=False, null=False, default='KG')


class WishlistProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="wishlist_user_product")
    class Meta:
        constraints = [models.UniqueConstraint(fields=['product', 'user'], name='user_product_unique')]


class Cuisine(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    image_url = models.CharField(max_length=500, null=True, blank=True)

class Meals(models.Model):

    STATUS_CHOICE = [
        (1, 'Breakfast'),
        (2, 'Lunch'),
        (3, 'Dinner'),
    ]
    TYPE_CHOICE = [
        (1, 'Very Easy'),
        (2, 'Easy'),
        (3, 'Medium')
    ]
    name = models.CharField(max_length=1000, null=True, blank=True)
    subtitle = models.CharField(max_length=1000, null=True, blank=True)
    category = models.ForeignKey(Cuisine, on_delete=models.CASCADE)
    image_url = models.CharField(max_length=1000, null=True, blank=True)
    recipe_type = models.SlugField(choices=TYPE_CHOICE, max_length=2, null=True, blank=True)
    recipe_time = models.CharField(max_length=100, null=True, blank=True)
    servings = models.IntegerField(null=True, blank=True)
    details = models.TextField(null=True, blank=True)
    ingredients = models.JSONField(null = True , blank = True , default = None)
    steps = models.JSONField(null = True , blank = True , default = None)
    meal_type = models.SlugField(choices=STATUS_CHOICE, max_length=2, null=True, blank=True)

class FavRecipes(models.Model):
    recipes = models.ForeignKey(Meals, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="wishlist_user_recipes")
    class Meta:
        constraints = [models.UniqueConstraint(fields=['recipes', 'user'], name='user_recipes_unique')]



