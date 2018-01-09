from django import template
from django.utils import html
register = template.Library()

class DeferHtml(template.Node):
    def __init__(self, nodelist):
        self.nodelist = nodelist

    def render(self, context):
        context['append_defer_html'](self.nodelist.render(context))
        return ''

@register.tag
def defer_html(parser, token):
    nodelist = parser.parse(('end_defer_html',))
    parser.delete_first_token()
    return DeferHtml(nodelist)

@register.simple_tag(takes_context=True)
def render_defer_html(context):
    res = ''
    for node in context['get_defer_html']():
        res += node
    return html.mark_safe(res)
