# Generated by Django 2.0 on 2018-01-27 14:20

import apps.projects.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0022_auto_20180125_1643'),
    ]

    operations = [
        migrations.AlterField(
            model_name='datarow',
            name='measuring_instrument',
            field=models.CharField(choices=[('Se', 'Sensor'), ('Ac', 'Actuator'), ('No', 'None')], default=apps.projects.models.MeasurementInstruments('No'), max_length=2),
        ),
    ]