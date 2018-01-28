from django.apps import AppConfig

from django.utils.translation import gettext_lazy as _

class ProfileConfig(AppConfig):
    name = 'apps.profile'
    verbose_name = _('profile')
