# Generated by Django 4.2 on 2025-01-29 18:13

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('brand', models.CharField(blank=True, max_length=100, null=True)),
                ('category', models.CharField(choices=[('DAIRY', 'Dairy'), ('MEAT AND FISH', 'Meat and Fish'), ('VEGETABLE', 'Vegetable'), ('FRUIT', 'Fruit'), ('GRAIN', 'Grain'), ('OTHER', 'Other')], max_length=20)),
                ('standard_expiry_days', models.IntegerField(blank=True, null=True)),
                ('allergy_tags', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(choices=[('DAIRY', 'Dairy'), ('NUTS', 'Nuts'), ('GLUTEN', 'Gluten'), ('SOY', 'Soy'), ('SHELLFISH', 'Shellfish'), ('EGG', 'Egg'), ('NONE', 'None')], max_length=50), blank=True, null=True, size=None)),
                ('quantity_type', models.CharField(choices=[('KG', 'Kilogram'), ('GRAM', 'Gram'), ('LITRE', 'Litre'), ('ML', 'Millilitre'), ('PIECE', 'Piece')], max_length=50)),
            ],
        ),
    ]
