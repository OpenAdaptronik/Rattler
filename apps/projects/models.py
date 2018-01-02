from django.db import models
from django.conf import settings

'''crates model Projects with
userId as ForeignKey from User
name as CharField
category as ForeignKey from Category
subcategory as ForeignKey from Subategory
producer as CharField
typ as CharField
note as TextField
'''


class Project(models.Model):
    projectID = models.IntegerField(primary_key=True)
    userID = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,)
    project_visibility = models.BooleanField(default=True)
    name = models.CharField(max_length=100, unique=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='projects_category_set')
    subcategory = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='projects_subcategory_set')
    manufacturer = models.CharField(max_length=100)
    typ = models.CharField(max_length=100)
    description = models.TextField(max_length=500)
    created = models.DateTimeField
    updated = models.DateTimeField


'''creates model Category with
categoryID as PrimaryKey
name as CharField
parent as Foreignkey from itself'''


class Category(models.Model):
    categoryID = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE,)


class ProjectImage(models.Model):
    project_imageID = models.IntegerField(primary_key=True)
    projectID = models.ForeignKey('Project', on_delete=models.CASCADE,)
    image = models.ImageField
