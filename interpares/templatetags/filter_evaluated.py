from django import template
from interpares.models import Griglia
register = template.Library()

@register.filter(name='evaluated')
def evaluated(tema, user):
    return Griglia.objects.filter(user=user, tema=tema).first()
