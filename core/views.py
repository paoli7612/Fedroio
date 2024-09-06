from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.urls import reverse
from .models import User
from .forms import UserForm

# Create your views here.
def account(request):
    return render(request, 'registration/account.html', {
        'answers': request.user.answers.all().order_by('-wrongly', 'correctly')
    })

def signup(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  
            return redirect(reverse('account'))
    else:
        form = UserForm()
    return render(request, 'registration/signup.html', {
        'form': form
    })