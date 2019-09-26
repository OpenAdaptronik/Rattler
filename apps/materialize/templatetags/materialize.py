from functools import wraps
from django import template
from django.forms.fields import TextInput
from django.utils import html
from django.utils.translation import gettext_lazy as _

register = template.Library()

def append_attr(field, attr_name, attr_value):
    if field.field.widget.attrs.get(attr_name, False):
        field.field.widget.attrs[attr_name] += ' %s' % attr_value
    else:
        field.field.widget.attrs[attr_name] = attr_value

def wrap_input_field_div(func=None, input_field=True):
    if input_field:
        template = '<div class="input-field col s{}">{}</div>'
    else:
        template = '<div class="col s{}">{}</div>'

    def dec(func):
        def wrapper(field, col=12, **flags):
            return html.format_html(
                template,
                col,
                html.mark_safe(func(field, **flags))
            )
            return template % (col, func(field, **flags))
        return wrapper

    if func is None:
        return dec
    else:
        return dec(func)

def form_field_type(field):
    if hasattr(field, 'field') and hasattr(field.field, 'widget') and field.field.widget:
        return field.field.widget.__class__.__name__.lower()
    return ''

@register.simple_tag(takes_context=False)
def materialize_form_field_label(field):
    id_for_label = getattr(field, 'id_for_label')
    label = getattr(field.field, 'label')
    if label is None:
        label = getattr(field, 'name')

    if field.errors:
        error = field.errors[0]
    else:
        error = ''

    if not label is None:
        return html.format_html(
            '<label for="{}" data-error="{}">{}</label>',
            id_for_label,
            error,
            label
        )
    return ''

@register.simple_tag(takes_context=False)
@wrap_input_field_div
def materialize_form_textinput(field):
    return html.mark_safe('%s%s' % (str(field), materialize_form_field_label(field)))

@register.simple_tag(takes_context=False)
@wrap_input_field_div
def materialize_form_textarea(field):
    append_attr(field, 'class', 'materialize-textarea')
    return html.mark_safe('%s%s' % (materialize_form_field_label(field), str(field)))

@register.simple_tag(takes_context=False)
@wrap_input_field_div
def materialize_form_select(field):
    return html.mark_safe('%s%s' % (str(field), materialize_form_field_label(field)))

@register.simple_tag(takes_context=False)
@wrap_input_field_div(input_field=False)
def materialize_form_checkboxinput(field):
    append_attr(field, 'class', 'filled-in')
    return html.mark_safe('%s%s' % (str(field), materialize_form_field_label(field)))

@register.simple_tag(takes_context=False)
@register.filter(is_save=True, takes_context=False)
def form_field_render(field, col=12, **kwargs):
    append_attr(field, 'class', 'validate')
    if field.errors:
        append_attr(field, 'class', 'invalid')
        append_attr(field, 'placeholder', '')

    return {
        'textinput': materialize_form_textinput,
        'textarea': materialize_form_textarea,
        'select': materialize_form_select,
        'checkboxinput': materialize_form_checkboxinput,
    }.get(
        form_field_type(field),
        materialize_form_textinput
    )(field, col, **kwargs)


@register.simple_tag(takes_context=True)
def form_add_javascript(context):
    return template.loader.render_to_string(
        'form/javascript.html'
    )

@register.filter(is_safe=True)
def materialize(form):
    return template.loader.render_to_string(
        'form/form.html',
        {
            'form': form
        }
    )

@register.simple_tag
def materialize_form_submit_btn(text=None):
    if text is None:
        text = _('save')
    return template.loader.render_to_string(
        'form/element/submit.html',
        {
            'text': text
        }
    )

@register.simple_tag(takes_context=False)
def materialize_paginator(paginator, url_name, params=None, buffer=9):
    current = paginator.number
    last = paginator.paginator.num_pages

    mb = 2 * buffer
    before_range = min(
        current - 1,
        max(
            mb - min(buffer, last - current),
            buffer
        )
    )
    after_range = min(
        last-current,
        max(
            mb - min(buffer, current-1),
            buffer
        )
    )

    return template.loader.render_to_string(
        'materialize/paginator.html',
        {
            'url_name': url_name,
            'has_previous': paginator.has_previous,
            'previous': paginator.previous_page_number,
            'pages_before': [n + current - before_range for n in range(before_range)],
            'current': paginator.number,
            'pages_after': [n + current + 1 for n in range(after_range)],
            'has_next': paginator.has_next,
            'next': paginator.next_page_number,
            'params': params
        }
    )
