from django.db import models
from django.conf import settings


# Create your models here.

class Profile(models.Model):
    profileID = models.IntegerField(primary_key=True)
    userID = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, )
    userImageID = models.ForeignKey('UserImage', on_delete=models.CASCADE,)
    company = models.CharField(max_length=255, null=True, blank=True)
    info = models.CharField(max_length=255, null=True, blank=True)
    expert = models.BooleanField(default=False)
    visibility_mail = models.BooleanField(default=False)
    visibility_company = models.BooleanField(default=False)
    visibility_info = models.BooleanField(default=False)
    max_projects = models.IntegerField(default=5)
    max_datarows = models.IntegerField(default=1000)
    created = models.DateTimeField
    updated = models.DateTimeField


    def curruser_company_finder(self):
        return self.objects.filter(userID=user.id).values['company']


class UserImage(models.Model):
    userImageID = models.IntegerField(primary_key=True)
    type = models.CharField(max_length=255, unique=True, default=None)
    data = models.ImageField
    created = models.DateTimeField
    updated = models.DateTimeField

