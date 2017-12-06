from django.db import models
from django.conf import settings


class Projects(models.Model):
    userID = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,)

    name = models.CharField(max_length=100, unique=True)
    kategorie = models.CharField(max_length=100)
    unterkategorie = models.CharField(max_length=100)
    hersteller = models.CharField(max_length=100)
    typ = models.CharField(max_length=100)
    notiz = models.TextField(max_length=500)



