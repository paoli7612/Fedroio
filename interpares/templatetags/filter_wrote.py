from django import template
from interpares.models import Tema
register = template.Library()

@register.filter(name='wrote')
def wrote(user, traccia):
    return Tema.objects.filter(user=user, traccia=traccia).first()
