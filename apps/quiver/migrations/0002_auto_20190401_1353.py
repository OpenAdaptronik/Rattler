# Generated by Django 2.0 on 2019-04-01 13:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiver', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='analyticsservice',
            name='api_key',
            field=models.CharField(max_length=100, verbose_name='api_key'),
        ),
    ]