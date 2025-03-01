# Generated by Django 4.2 on 2025-02-28 18:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('custom_auth', '0016_entry_quantity_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meals',
            name='meal_type',
            field=models.SlugField(blank=True, choices=[(1, 'Breakfast'), (2, 'Lunch'), (3, 'Dinner')], max_length=2, null=True),
        ),
    ]
