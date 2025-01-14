from django.db import models
from django.contrib.postgres.fields import ArrayField
from user.enums import PreferencesTags, GenderChoices
from product.models import Product



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

class UserProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user_id = models.IntegerField()
    @property
    def total_quantity(self):
        return sum(entry.quantity for entry in self.entry_set.all())

class Entry(models.Model):
    user_inventory = models.ForeignKey(UserProduct, on_delete=models.CASCADE)
    quantity = models.FloatField()
    expiry_date = models.DateField()
    creation_date = models.DateField(auto_now_add=True)  




