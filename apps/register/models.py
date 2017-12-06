from django.conf import settings
from django.db import models

from django.contrib.auth.tokens import default_token_generator

class VerificationTokenManager(models.Manager):
    def create_user_token(self, user):
        if hasattr(user, 'verificationtoken'):
            return user.verificationtoken.token

        token = self.model(
            user=user,
            token = default_token_generator.make_token(user)
        )

        token.save()
        return token.token

class VerificationToken(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, unique=True)
    token = models.CharField(max_length=255, unique=True)

    objects = VerificationTokenManager()
