# Generated by Django 4.1 on 2023-06-08 12:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_userprofile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='followers',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='profile_picture',
        ),
    ]
