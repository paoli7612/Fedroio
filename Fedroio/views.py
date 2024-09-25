from django.shortcuts import render, redirect
from django.urls import reverse
from pawns.models import Pawn
from pawns.models import Question

def index(request):
    return redirect(reverse('home'))

def home(request):
    return render(request, 'index.html', {
        'pawns': Pawn.objects.filter(parent=None, is_public=True)[:2]
    })

def info(request):
    return render(request, 'info.html', {
        'questions': Question.objects.all()
    })
