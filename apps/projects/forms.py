from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Project, Category, ProjectImage

class ProjectForm(forms.ModelForm):
    category = forms.ModelChoiceField(Category.objects.filter(parent=None), label=_('category'))
    subcategory = forms.ChoiceField(label=_('subcategory'))
    new_subcategory = forms.CharField(required=False, label=_('new subcategory'))

    field_order = (
        'name',
        'category',
        'subcategory',
        'new_subcategory',
        'manufacturer',
        'typ',
        'description',
        'visibility',
    )
    
    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)
        self.fields['subcategory'].choices = self.get_subcategory_choices()

    def get_subcategory_choices(self):
        choices = [(None, '---------')]
        choices += [(0, 'new subcategory')]
        category = self.data.get('category', False)

        if not category and self.instance and hasattr(self.instance, 'category'):
            category = self.instance.category

        if category:
            subcategories = Category.objects.allDescandends(parent=category)
            subcategories = subcategories.order_by('id')
            choices += [(c.id, c.name) for c in subcategories]

        return choices

    def clan_new_subcategory(self):
        category = self.cleaned_data['category']
        subcategory = self.data.get('subcategory', '0')

        if not subcategory == '0':
            return None

        new_subcategory = self.cleaned_data.get(
            'new_subcategory', 
            self.data.get('new_subcategory', None)
        )

        if not new_subcategory:
            raise forms.ValidationError(
                'Required',
                code='required'
            )

        try:
            new_category = Category.objects.get(name=new_subcategory, parent=category)
        except Category.DoesNotExist:
            new_category = Category(name=new_subcategory, parent=category)
            new_category.save()

        return new_category

    def clean_subcategory(self):
        subcategory = self.cleaned_data['subcategory']

        if subcategory == '0':
            return self.clan_new_subcategory()

        try:
            data = Category.objects.get(id=subcategory)
        except Category.DoesNotExist:
            raise forms.ValidationError('foo')

        return data

    class Meta:
        """ Meta informations.
        """
        model = Project
        fields = (
            'name',
            'category',
            'subcategory',
            'manufacturer',
            'typ',
            'description',
            'visibility',
        )

class ProjectImageForm(forms.ModelForm):
    class Meta:
        model = ProjectImage
        fields = ['path']


ProjectImageCreateFormSet = forms.inlineformset_factory(
    Project,
    ProjectImage,
    fk_name='project',
    form=ProjectImageForm,
    extra=3,
    fields=('path',),
    can_delete=False,
)

ProjectImageFormSet = forms.inlineformset_factory(
    Project,
    ProjectImage,
    fk_name='project',
    form=ProjectImageForm,
    extra=3,
    fields=('path',)
)
