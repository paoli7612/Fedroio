from django.shortcuts import render

def account(request):
    return render(request, 'registration/account.html')