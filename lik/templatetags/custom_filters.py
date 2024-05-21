from django import template

register = template.Library()

@register.filter(name='strip_spaces')
def strip_spaces(value):
    if value is not None:
        return value.replace(" ","")
    return value