from django import template
from pawns.models import OpenAnswer

register = template.Library()

@register.filter(name='canAnswer')
def canAnswer(pawn, user):
    user_groups = user.groups.all()
    pawn_groups = pawn.groups.all()
    return user_groups.filter(id__in=pawn_groups).exists()


