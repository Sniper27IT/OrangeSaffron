# Generated by Django 4.1 on 2023-06-10 10:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0007_userprofile_followers_alter_recipe_category'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='followers',
        ),
    ]