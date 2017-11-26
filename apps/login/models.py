from django.db import models

# Create your models here.

# Create your models here.
class User(models.Model):
    #userID = models.IntegerField()
    username = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    salt = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.userID
