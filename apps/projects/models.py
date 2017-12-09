from django.db import models
from django.conf import settings


class Projects(models.Model):
    userID = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,)

    name = models.CharField(max_length=100, unique=True)
    category = models.CharField(max_length=100)
    subcategory = models.CharField(max_length=100)
    producer = models.CharField(max_length=100)
    typ = models.CharField(max_length=100)
    note = models.TextField(max_length=500)


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

class Subcategory(models.Model):
    name = models.CharField(max_length=100, unique=True)

class Producer(models.Model):
    name = models.CharField(max_length=100, unique=True)

class Typ(models.Model):
    name = models.CharField(max_length=100, unique=True)
