from django.db import models
from .enums import Categories, QuantityType
from django.db.models import JSONField

class Product(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False,unique=True)
    # brand = models.CharField(max_length=100, blank=True, null=True)
    category = models.CharField(max_length=20, choices=Categories.choices, blank=False, null=False)
    tags = JSONField(blank=True, null=True)
    standard_expiry_days = models.IntegerField(blank=True, null=True)
    allergy_tags = JSONField(blank=True, null=True, default=dict)
    # quantity_type = models.CharField(max_length=50, choices=QuantityType.choices, blank=False, null=False)