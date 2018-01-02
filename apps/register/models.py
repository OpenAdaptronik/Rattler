from django.conf import settings
from django.db import models
from django.db import IntegrityError

from django.contrib.auth.tokens import default_token_generator


class VerificationTokenManager(models.Manager):
    """Verification token manager
    
    Handles default methods for token generation and verification
    """
    
    def create_user_token(self, user):
        if hasattr(user, 'verificationtoken'):
            return user.verificationtoken.token

        token = self.model(
            user=user,
            token=default_token_generator.make_token(user)
        )
        try:
            print(token.token)
            token.save()
        except IntegrityError:
            print("FEHLER")
            VerificationTokenManager.create_user_token(self,user)
        return token.token

    def get_token(self, token):
        try:
            return self.model.objects.get(token=token)
        except self.model.DoesNotExist:
            return None 

    def verify_user(self, user):
        user.is_active = True
        user.save()


class VerificationToken(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,)
    token = models.CharField(max_length=255, unique=True)

    objects = VerificationTokenManager()
