# Generated by Django 2.0 on 2019-04-08 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiver', '0002_auto_20190401_1353'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='analyticsservice',
            options={'verbose_name': 'analytics_service', 'verbose_name_plural': 'analytics_services'},
        ),
        migrations.AddField(
            model_name='analyticsservice',
            name='visibility',
            field=models.BooleanField(default=True, verbose_name='visibility'),
        ),
    ]