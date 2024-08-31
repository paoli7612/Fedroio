from django.shortcuts import render, redirect
from django.urls import reverse

def index(request):
    return redirect(reverse('home'))

def home(request):
    return render(request, 'index.html')

def account(request):
    return render(request, 'registration/account.html')

def info(request):
    return render(request, 'info.html')