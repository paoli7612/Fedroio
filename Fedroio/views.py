from django.shortcuts import render, redirect
from django.urls import reverse
from pawns.models import Pawn, Question, Sentence

def index(request):
    return redirect(reverse('home'))

def home(request):
    return render(request, 'index.html', {
        'pawns': Pawn.objects.filter(parent=None, public=True).order_by('?')[:2]
    })

def info(request):
    return render(request, 'info.html', {
        'questions': Question.objects.all(),
        'sentences': Sentence.objects.all()
    })
