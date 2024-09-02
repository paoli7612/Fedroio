from django import template

register = template.Library()

@register.filter(name='split')
def split(value, key=' '):
    return value.split(key)

@register.filter(name='start_with')
def start_with(value, key):
    return str(value).startswith(key)