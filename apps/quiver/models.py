import os
from django.db import models
from django.conf import settings
from django.shortcuts import reverse
from django.utils.encoding import iri_to_uri
from django.utils.translation import gettext_lazy as _

from django.utils.timezone import now


# Create your models here.
class AnalyticsService(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('user'), on_delete=models.CASCADE,)
    name = models.CharField(_('name'), max_length=100)
    description = models.TextField(_('description'), max_length=500)
    url = models.CharField(_('url'), max_length=100)
    api_key = models.CharField(_('api_key'), max_length=100)
    visibility = models.BooleanField(_('visibility'), default=True)
    updated = models.DateTimeField(_('updated'), auto_now=True)

    class Meta:
        verbose_name = _('analytics_service')
        verbose_name_plural = _('analytics_services')

    def get_absolute_url(self):
        kwargs = {
            'id': self.id,
            'name': iri_to_uri(self.name)
        }
        return reverse('quiver:detail', kwargs=kwargs)


class AnalyticsServiceExecution(models.Model):
    service = models.ForeignKey('AnalyticsService', on_delete=models.CASCADE, default=0)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('user'), on_delete=models.CASCADE,)
    last_state = models.IntegerField(default=1)
    last_contact = models.DateTimeField(default=now, blank=True)
