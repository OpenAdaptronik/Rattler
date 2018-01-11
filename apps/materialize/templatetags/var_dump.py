from django import template
register = template.Library()

@register.simple_tag(takes_context=False)
def var_dump(var):
    if isinstance(var, dict):
        return vars(var)
    else:
        return vars({'var': var})
