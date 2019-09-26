from django import forms
from django.utils.translation import gettext_lazy as _

from .models import AnalyticsService

class AnalyticsServiceForm(forms.ModelForm):

    field_order = (
        'name',
        'description',
        'url',
        'api_key',
        'visibility',
    )

    def __init__(self, *args, **kwargs):
        super(AnalyticsServiceForm, self).__init__(*args, **kwargs)

    class Meta:
        model = AnalyticsService
        fields = (
            'name',
            'description',
            'url',
            'api_key',
            'visibility',
        )
