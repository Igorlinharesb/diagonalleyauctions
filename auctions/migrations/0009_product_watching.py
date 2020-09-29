# Generated by Django 3.1 on 2020-08-18 19:56

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_auto_20200816_2010'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='watching',
            field=models.ManyToManyField(blank=True, related_name='watchlist', to=settings.AUTH_USER_MODEL),
        ),
    ]
