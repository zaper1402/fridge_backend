from django.db import models
from .enums import Categories, QuantityType, AllergyTags
from django.contrib.postgres.fields import ArrayField


class Product(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)
    # brand = models.CharField(max_length=100, blank=True, null=True)
    category = models.CharField(max_length=20, choices=Categories.choices, blank=False, null=False)
    standard_expiry_days = models.IntegerField(blank=True, null=True)
    allergy_tags = ArrayField(models.CharField(max_length=50, choices=AllergyTags.choices), blank=True, null=True)
    # quantity_type = models.CharField(max_length=50, choices=QuantityType.choices, blank=False, null=False, default='KG')