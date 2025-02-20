from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('custom_auth', '0013_userproduct_subname'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cuisine',
            name='image_url',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='meals',
            name='image_url',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='meals',
            name='recipe_type',
            field=models.SlugField(blank=True, choices=[(1, 'Very Easy'), (2, 'Easy'), (3, 'Medium')], max_length=2, null=True),
        ),
    ]
