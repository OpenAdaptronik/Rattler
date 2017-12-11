from django.forms import BaseForm as django_BaseForm

class BaseForm(django_BaseForm):
    def __init__(self, *args,**kwargs):
        super(BaseForm, self).__init__(*args, **kwargs)
        for v in self.visible_fields():
            v.field.widget.attrs['class'] = 'validate'


    def is_valid(self):
        valid = super(BaseForm, self).is_valid()
        if valid:
            return True
        for v in self.visible_fields():
            if v.field.error_messages is not None:
                v.field.widget.attrs['class'] += ' invalid'
        return False
