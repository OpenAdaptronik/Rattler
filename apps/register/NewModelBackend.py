from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

class NewModelBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            if '@' in username:
                UserModel.USERNAME_FIELD = 'email'
            else:
                UserModel.USERNAME_FIELD = 'username'

            user = UserModel._default_manager.get_by_natural_key(username)
        except UserModel.DoesNotExist:
            return None
        else:
            if user.check_password(password):
                return user
        return None