# Generated by Django 4.1 on 2023-06-08 13:54

from django.db import migrations


def create_default_categories(apps, schema_editor):

    Category = apps.get_model('recipes', 'Category')

    categories = [
        {'name': '(empty)', 'description': 'No category'},
        {'name': 'Breakfast', 'description': 'Delicious breakfast recipes'},
        {'name': 'Lunch', 'description': 'Tasty lunch ideas'},
        {'name': 'Dinner', 'description': 'Satisfying dinner recipes'},
        {'name': 'Dessert', 'description': 'Sweet treats'},
        {'name': 'Snack', 'description': 'Quick and easy snacks'},
        {'name': 'Appetizer', 'description': 'Appetizers for any occasion'},
        {'name': 'Beverage', 'description': 'Refreshing drinks'},
        {'name': 'Side Dish', 'description': 'Side dishes to complement any meal'},
        {'name': 'First Course', 'description': 'First course recipes'},
        {'name': 'Main Course', 'description': 'Main course recipes'},
        {'name': 'Cocktails', 'description': 'Cocktails for any occasion'},
        {'name': 'Vegetarian', 'description': 'Vegetarian recipes'},
        {'name': 'Vegan', 'description': 'Vegan recipes'},
    ]

    for category_data in categories:
        Category.objects.create(**category_data)


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0004_category_description_alter_category_name'),
    ]

    operations = [
        migrations.RunPython(create_default_categories),
    ]
