# Generated by Django 3.2 on 2023-01-21 11:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0002_review'),
    ]

    operations = [
        migrations.RenameField(
            model_name='review',
            old_name='rating',
            new_name='score',
        ),
    ]
