from django.shortcuts import render

def account(request):
    return render(request, 'registration/account.html')

def index(request):
    return render(request, 'index.html')

def info(request):
    return render(request, 'info.html')