from django.shortcuts import render, get_object_or_404
from pawns.models import Pawn

# Create your views here.
def pawn(request, uuid):
    pawn = get_object_or_404(Pawn, uuid=uuid)
    return render(request, 'explore/pawn.html', {
        'pawn': pawn
    })