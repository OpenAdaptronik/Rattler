# Generated by Django 2.0 on 2018-05-17 10:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0003_auto_20180427_0823'),
    ]

    operations = [
        migrations.AlterField(
            model_name='experiment',
            name='description',
            field=models.TextField(max_length=2500, null=True, verbose_name='description'),
        ),
    ]