from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.models import Group
from django.urls import reverse
from .models import User
from .forms import UserForm, GroupMembersForm, SettingsForm
from .decorators import admin_required, login_required
from pawns.models import Pawn

# Create your views here.
@login_required
def account(request):
    return render(request, 'registration/account.html', {
        'user': request.user
    })

@login_required
def settings(request):
    user = request.user

    if request.method == 'POST':
        form = SettingsForm(request.POST)
        if form.is_valid():
            user.theme = form.cleaned_data['theme']
            user.save()
            return redirect('account')
    else:
        form = SettingsForm(initial={'theme': user.theme})

    return render(request, 'registration/settings.html', {
        'form': form
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
def user_reset(request, username):
    user = get_object_or_404(User, username=username)
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
    from pawns.models import Question
    return render(request, 'dashboard.html', {
        'users': User.objects.filter(is_superuser=False),
        'groups': Group.objects.all(),
        'questions': Question.objects.all()
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
        form = GroupMembersForm(request.POST)
        if form.is_valid():
            form.save()  
            return redirect('dashboard')  
    else:
        form = GroupMembersForm()
    
    return render(request, 'admin/form.html', {'form': form})


def group_partis_reset(request, id, pawn_id):
    pawn = get_object_or_404(Pawn, id=pawn_id)
    for question in pawn.openQuestions.all():
        question.answers.all().delete()
    messages.success(request, 'Risposte cancellate')
    return redirect(reverse('core.group.partis', kwargs={'id': id}))

def group_partis_stats(request, id, pawn_id):
    messages.info(request, 'success')
    return render(request, 'admin/group-partis-stats.html', {
        'group': get_object_or_404(Group, id=id)
    })




def group_partis(request, id):
    group = get_object_or_404(Group, id=id)

    if request.method == 'POST':
        pawn_id = request.POST.get('pawn_id')
        pawn = get_object_or_404(Pawn, id=pawn_id)
        if pawn.partis_run:
            pawn.partis_run = False
            messages.info(request, 'Autovalutazione disattivata')
        else:
            pawn.partis_run = True
            messages.info(request, 'Autovalutazione attivata')

        pawn.save()
        return redirect(reverse('core.group.partis', kwargs={'id': id}))

    return render(request, 'admin/group-partis.html', {
        'group': group
    })