# Generated by Django 3.2 on 2023-05-06 18:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0004_auto_20230506_1952'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='user',
            name='unique_user',
        ),
        migrations.RemoveConstraint(
            model_name='user',
            name='username_is_not_me',
        ),
    ]
