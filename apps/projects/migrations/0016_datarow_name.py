# Generated by Django 2.0 on 2018-01-20 12:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0015_auto_20180113_1717'),
    ]

    operations = [
        migrations.AddField(
            model_name='datarow',
            name='name',
            field=models.CharField(max_length=10, null=True),
        ),
    ]