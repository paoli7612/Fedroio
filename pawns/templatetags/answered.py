from django import template
from pawns.models import OpenAnswer

register = template.Library()

@register.filter(name='answered')
def start_with(question, user):
    return OpenAnswer.objects.filter(user=user, openQuestion=question).exists()

