from django.db import models
from django.conf import settings

'''crates model Projects with
userId as ForeighKey from User
name as CharField
category as ForeignKey from Category
subcategory as ForeignKey from Subategory
producer as CharField
typ as CharField
note as TextField
'''
class Projects(models.Model):
    userID = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,)

    name = models.CharField(max_length=100, unique=True)
    category = models.ForeignKey(
        'Category',
        on_delete=models.CASCADE,
        related_name='projects_category_set'
    )
    subcategory = models.ForeignKey(
        'Category',
        on_delete=models.CASCADE,
        related_name='projects_subcategory_set'
    )
    producer = models.CharField(max_length=100)
    typ = models.CharField(max_length=100)
    note = models.TextField(max_length=500)

'''creates model Category with
categoryID as PrimaryKey
name as CharField
parent as Foreignkey from itself'''
class Category(models.Model):
    categoryID = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    parent = models.ForeignKey('self',
                               on_delete=models.CASCADE,
                               )

