from django.db import models
from django.contrib.auth.models import Group, Permission
from django.contrib.postgres.fields import ArrayField
from user.enums import PreferencesTags, GenderChoices
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, AbstractUser
from product.models import Product
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import password_validation
from django.contrib.auth.hashers import (
    check_password,
    is_password_usable,
    make_password,
)
from product.enums import QuantityType
from django.utils.timezone import now


class User(AbstractUser):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=10, choices=GenderChoices.choices, blank=True, null=True)
    photo = models.ImageField(upload_to='photos/', blank=True, null=True)
    preferences = ArrayField(
        models.CharField(max_length=20, choices=PreferencesTags.choices),
        blank=True,
        null=True
    )

    def save(self, *args, **kwargs):
        self.password = make_password(self.password)
        super().save(*args, **kwargs)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']
    

    class Meta:
        db_table = 'user_user'
        swappable = 'AUTH_USER_MODEL'

    def __str__(self):
        return self.email

class UserProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=False, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)
    brand = models.CharField(max_length=100, blank=True, null=True)
    expiry_date = models.DateField()
    quantity = models.FloatField()
    quantity_type = models.CharField(max_length=50, choices=QuantityType.choices, blank=False, null=False)
    @property
    def total_quantity(self):
        return sum(entry.quantity for entry in self.entry_set.all())
    
    class Meta:
        db_table = 'user_userproduct'

class Entry(models.Model):
    user_inventory = models.ForeignKey(UserProduct, on_delete=models.CASCADE)
    quantity = models.FloatField()
    expiry_date = models.DateField()
    creation_date = models.DateField(auto_now_add=True)  

    class Meta:
        db_table = 'user_entry'




