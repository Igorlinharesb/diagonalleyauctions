# Generated by Django 3.1 on 2020-08-15 20:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_comments'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Bids',
            new_name='Bid',
        ),
        migrations.RenameModel(
            old_name='Comments',
            new_name='Comment',
        ),
    ]