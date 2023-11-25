# Generated by Django 4.2.2 on 2023-10-24 02:02

from django.conf import settings
import django.contrib.auth
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('boards', '0005_alter_city_city_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='user',
            field=models.ForeignKey(
    to=settings.AUTH_USER_MODEL,
    on_delete=django.db.models.deletion.CASCADE,
    null=True,
        ),
        )
    ]