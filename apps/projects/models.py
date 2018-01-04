from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.shortcuts import reverse

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

    def get_absolute_url(self):
        kwargs = {
            'id': self.id,
            'name': self.name
        }
        return reverse('projects:detail', kwargs=kwargs)

    def __str__(self):
        return self.name    


'''creates model Category with
categoryID as PrimaryKey
name as CharField
parent as Foreignkey from itself'''


class Category(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE,)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ('name', 'parent',)

def project_image_path(instance, filename):
    return 'project/%s%s' % (instance.project.id, os.path.splitext(filename)[1])

class ProjectImage(models.Model):
    project = models.ForeignKey('Project', on_delete=models.CASCADE,)
    path = models.ImageField(upload_to=project_image_path)

class Experiment(models.Model):
    experiment = models.IntegerField(primary_key=True),
    project = models.ForeignKey('Project', on_delete=models.CASCADE,),
    performed_on = models.DateField,
    description = models.TextField(max_length=500)

class Datarow(models.Model):
    datarow = models.IntegerField(primary_key=True),
    experiment = models.ForeignKey('Experiment', on_delete=models.CASCADE,),
    unit = models.CharField(max_length=10),
    description = models.TextField(max_length=500)

class Value(models.Model):
    id = models.IntegerField(primary_key=True),
    datarow = models.ForeignKey('Datarow', on_delete=models.CASCADE,),
    value = models.IntegerField()
