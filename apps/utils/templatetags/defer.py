from django import template
from django.utils import html
register = template.Library()

def _collect(context, name):
    res = ''
    for node in context[name]():
        res += node
    return res

class DeferHtml(template.Node):
    def __init__(self, nodelist):
        self.nodelist = nodelist

    def render(self, context):
        context['append_defer_html'](self.nodelist.render(context))
        return ''

class DeferHead(template.Node):
    def __init__(self, nodelist):
        self.nodelist = nodelist

    def render(self, context):
        context['append_defer_head'](self.nodelist.render(context))
        return ''

@register.tag
def defer_html(parser, token):
    nodelist = parser.parse(('end_defer_html',))
    parser.delete_first_token()
    return DeferHtml(nodelist)

@register.simple_tag(takes_context=True)
def render_defer_html(context):
    return html.mark_safe(_collect(context, 'get_defer_html'))

@register.tag
def defer_head(parser, token):
    nodelist = parser.parse(('end_defer_head',))
    parser.delete_first_token()
    return DeferHead(nodelist)

@register.simple_tag(takes_context=True)
def render_defer_head(context):
    return html.mark_safe(_collect(context, 'get_defer_head'))
