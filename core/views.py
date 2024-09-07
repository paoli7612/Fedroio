from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.models import Group
from django.urls import reverse
from .models import User
from .forms import UserForm, GroupMembersForm
from .decorators import admin_required

# Create your views here.
def account(request):
    return render(request, 'registration/user.html', {
        'user': request.user
    })

def user(request, username):
    return render(request, 'registration/user.html', {
        'user': get_object_or_404(User, username=username)
    })

@admin_required
def user_delete(request, username):
    user = get_object_or_404(User, username=username)
    if request.method == 'POST':
        user.delete()
        return redirect(reverse('dashboard'))
    return render(request, 'ask.html', {
        'title': 'Delete Pawn',
        'text': f'You\'re deleting the User: <b>{user}</b>?',
        'url_back': reverse('dashboard')
    })

@admin_required
def group_delete(request, username):
    group = get_object_or_404(Group, username=username)
    if request.method == 'POST':
        group.delete()
        return redirect(reverse('dashboard'))
    return render(request, 'ask.html', {
        'title': 'Delete Pawn',
        'text': f'You\'re deleting the Group: <b>{group}</b>?',
        'url_back': reverse('dashboard')
    })

@admin_required
def user_reset(request, id):
    user = get_object_or_404(User, id=id)
    password = user.reset_password()
    messages.success(request, f"{user}: new password = {password}")
    return redirect(reverse('dashboard'))

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

def dashboard(request):
    return render(request, 'dashboard.html', {
        'users': User.objects.filter(is_superuser=False),
        'groups': Group.objects.all()
    })

@admin_required
def group_edit(request, id):
    group = get_object_or_404(Group, id=id)
    
    if request.method == 'POST':
        form = GroupMembersForm(request.POST, instance=group)
        if form.is_valid():
            # Aggiorna i membri del gruppo
            users = form.cleaned_data['users']
            group.user_set.set(users)  # Aggiorna i partecipanti del gruppo
            return redirect('dashboard')  # Reindirizza alla lista dei gruppi o un'altra pagina desiderata
    else:
        form = GroupMembersForm(instance=group)  # Precompila il form con i partecipanti attuali
    
    return render(request, 'admin/form.html', {'form': form, 'group': group})

def group_new(request):
    if request.method == 'POST':
        # Se è un POST, stiamo creando un nuovo gruppo con i dati inviati
        form = GroupMembersForm(request.POST)
        if form.is_valid():
            form.save()  # Crea il nuovo gruppo e i membri associati
            return redirect('dashboard')  # Reindirizza alla pagina desiderata, es. 'dashboard'
    else:
        # Altrimenti, mostra un form vuoto per creare un nuovo gruppo
        form = GroupMembersForm()
    
    return render(request, 'admin/form.html', {'form': form})