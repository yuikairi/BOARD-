# Generated by Django 4.2.2 on 2023-10-19 11:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boards', '0004_post_total_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='city',
            name='city_name',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
