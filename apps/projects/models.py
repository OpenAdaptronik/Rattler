import os
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.shortcuts import reverse
from django.utils.encoding import iri_to_uri
from enum import Enum

'''crates model Projects with
userId as ForeignKey from User
name as CharField
category as ForeignKey from Category
subcategory as ForeignKey from Subategory
producer as CharField
typ as CharField
note as TextField
'''

class Project(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('user'), on_delete=models.CASCADE,)
    name = models.CharField(_('name'), max_length=100)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='projects_category_set', verbose_name=_('category'))
    subcategory = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='projects_subcategory_set', verbose_name=_('subcategory'))
    manufacturer = models.CharField(_('manufacturer'), max_length=100)
    typ = models.CharField(_('type'), max_length=100)
    description = models.TextField(_('description') ,max_length=500)
    visibility = models.BooleanField(_('visibility'), default=True)
    created = models.DateTimeField(_('created'), auto_now_add=True)
    updated = models.DateTimeField(_('updated'), auto_now=True)
    measured = models.DateTimeField(null=True)

    class Meta:
        verbose_name = _('project')
        verbose_name_plural = _('projects')

    def get_absolute_url(self):
        kwargs = {
            'id': self.id,
            'name': iri_to_uri(self.name)
        }
        return reverse('projects:detail', kwargs=kwargs)

    def __str__(self):
        return self.name    


'''creates model Category with
categoryID as PrimaryKey
name as CharField
parent as Foreignkey from itself'''


class Category(models.Model):
    name = models.CharField(_('name'), max_length=100)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, verbose_name=_('parent'))

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ('name', 'parent',)
        verbose_name = _('category')
        verbose_name_plural = _('categories')

def project_image_path(instance, filename):
    return 'project/%s/%s%s' % (instance.project.id, instance.project.name, os.path.splitext(filename)[1])

class ProjectImage(models.Model):
    project = models.ForeignKey('Project', on_delete=models.CASCADE,verbose_name=_('project'))
    path = models.ImageField(upload_to=project_image_path, verbose_name=_('path'))


class Experiment(models.Model):
    name = models.CharField(_('name'),max_length=100, null=True)
    project = models.ForeignKey('Project',on_delete=models.CASCADE, verbose_name=_('project'))
    created = models.DateTimeField(null=True, auto_now_add=True, verbose_name=_('created'))
    description = models.TextField(max_length=500, null=True, verbose_name=_('description'))
    timerow = models.IntegerField(null=True,verbose_name=_('timerow'))


class MeasurementInstruments(Enum):
    SENSOR = 'Se'
    ACTUATOR = 'Ac'
    NONE = 'No'


class Datarow(models.Model):
    experiment = models.ForeignKey('Experiment', on_delete=models.CASCADE, )
    unit = models.CharField(max_length=10, null=True, verbose_name=_('unit'))
    description = models.TextField(max_length=500, null=True, verbose_name=_('description'))
    unit = models.CharField(max_length=10, null=True)
    name = models.CharField(max_length=50, null=True)
    description = models.TextField(max_length=500, null=True)
    measuring_instrument = models.CharField(max_length=2,
                                            choices=tuple((x.name, x.value) for x in MeasurementInstruments),
                                            default=MeasurementInstruments.NONE)


class Value(models.Model):
    datarow = models.ForeignKey('Datarow', on_delete=models.CASCADE, verbose_name=_('datarow') )
    value = models.DecimalField(max_digits=20, decimal_places=15, null=True null=True, verbose_name=_('value'))
)
