import os
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.shortcuts import reverse
from django.utils.encoding import iri_to_uri
from enum import Enum
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone


'''creates model Projects with
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
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='projects_category_set',
                                 verbose_name=_('category'))
    subcategory = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='projects_subcategory_set',
                                    verbose_name=_('subcategory'))
    manufacturer = models.CharField(_('manufacturer'), max_length=100)
    typ = models.CharField(_('type'), max_length=100)
    description = models.TextField(_('description'), max_length=500)
    visibility = models.BooleanField(_('visibility'), default=True)
    created = models.DateTimeField(_('created'), auto_now_add=True)
    updated = models.DateTimeField(_('updated'), auto_now=True)
    

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


class CategoryManager(models.Manager):
    def childrenIds(self, parent):
        ids = []
        children = self.filter(parent=parent)
        for child in children:
            ids.append(child.pk)
            ids.extend(self.childrenIds(child))
        return ids

    def allDescandends(self, parent):
        return self.filter(id__in = self.childrenIds(parent)).order_by('name')

'''creates model Category with
categoryID as PrimaryKey
name as CharField
parent as Foreignkey from itself'''
class Category(models.Model):
    name = models.CharField(_('name'), max_length=100)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, verbose_name=_('parent'))

    objects = CategoryManager()
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

    class Meta:
        verbose_name = _('project image')
        verbose_name_plural = _('project images')



class Experiment(models.Model):
    name = models.CharField(_('name'),max_length=100, null=True)
    project = models.ForeignKey('Project',on_delete=models.CASCADE, verbose_name=_('project'))
    created = models.DateTimeField(null=True, auto_now_add=True, verbose_name=_('created'))
    description = models.TextField(max_length=500, null=True, verbose_name=_('description'))
    timerow = models.IntegerField(null=True,verbose_name=_('timerow'))
    measured = models.DateTimeField(null=True, verbose_name=_('measured'))

    class Meta:
        verbose_name = _('experiment')
        verbose_name_plural = _('experiments')


# Enum Model, damit man beim Auslesen von Datarow measuring_instrument besser auslesen kann;
# z.B. actor_datarows = Datarow.objects.filter(measuring_instruments = MeasuringInstruments.ACTUATOR)
class MeasurementInstruments(Enum):
    SENSOR = 'Se'
    ACTUATOR = 'Ac'
    NONE = 'No'



class Datarow(models.Model):
    name = models.CharField(_('name'), max_length=100, null=True)
    experiment = models.ForeignKey('Experiment', on_delete=models.CASCADE, )
    unit = models.CharField(max_length=10, null=True, verbose_name=_('unit'))
    description = models.TextField(max_length=500, null=True, verbose_name=_('description'))
    measuring_instrument = models.CharField(max_length=2,
                                            choices=tuple((x.name, x.value) for x in MeasurementInstruments),
                                            default=MeasurementInstruments.NONE, verbose_name=_('measuring instrument'))
    class Meta:
        verbose_name = _('datarow')
        verbose_name_plural = _('datarows')



class Value(models.Model):
    datarow = models.ForeignKey('Datarow', on_delete=models.CASCADE, verbose_name=_('datarow'))
    value = models.DecimalField(max_digits=20, decimal_places=15, null=True, verbose_name=_('value'))

@receiver(post_save, sender=Experiment)
def update_experiment(sender, instance, created, **kwargs):
    instance.project.updated = timezone.now()
    instance.project.save()
