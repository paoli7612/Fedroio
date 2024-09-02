from django.shortcuts import render, redirect
from django.urls import reverse
from pawns.models import Pawn

def index(request):
    return redirect(reverse('home'))

def home(request):
    return render(request, 'index.html', {
        'pawns': Pawn.objects.filter(parent=None)[:2]
    })

def account(request):
    return render(request, 'registration/account.html', {
        'answers': request.user.answers.all().order_by('-wrongly')
    })

def info(request):
    return render(request, 'info.html')