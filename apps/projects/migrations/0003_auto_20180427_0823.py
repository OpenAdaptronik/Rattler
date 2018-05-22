# Generated by Django 2.0 on 2018-04-27 08:23

from django.db import migrations

categories = [
    {
        'name': 'Sonstiges',
        'children': []
    },
]

def save(model, name, parent=None):
    try:
        entry = model.objects.get(name=name, parent=parent)
    except model.DoesNotExist:
        entry = model(name=name, parent=parent)
        entry.save()
    return entry

def add_categories(apps, schema_editor):
    Category = apps.get_model("projects", "Category")

    for category in categories:
        parent = save(Category, category['name'])
        for child in category['children']:
            save(Category, child, parent=parent)

def remove_categories(apps, schema_editor):
    Category = apps.get_model("projects", "Category")
    for category in categories:
        try:
            cat = Category.objects.get(name=category['name'])
            cat.delete()
        except:
            pass

class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0002_add_categories'),
    ]

    operations = [
        migrations.RunPython(add_categories, remove_categories)
    ]
