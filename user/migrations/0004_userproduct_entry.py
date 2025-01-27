# Generated by Django 5.1.2 on 2025-01-13 16:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
        ('user', '0003_remove_user_age_user_date_of_birth_user_gender'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField()),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.product')),
            ],
        ),
        migrations.CreateModel(
            name='Entry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.FloatField()),
                ('expiry_date', models.DateField()),
                ('creation_date', models.DateField(auto_now_add=True)),
                ('user_inventory', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.userproduct')),
            ],
        ),
    ]
