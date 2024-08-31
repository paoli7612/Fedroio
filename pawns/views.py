from django.shortcuts import render, get_object_or_404, redirect
from django.db import IntegrityError
from django.urls import reverse
from django.contrib import messages
from .models import Pawn
from .forms import PawnForm
from quiz.models import Question

# Create your views here.
def index(request):
    return render(request, 'pawns/index.html', {
        'pawns': Pawn.objects.filter(parent=None)
    })

def pawn(request, slug):
    pawn = get_object_or_404(Pawn, slug=slug)
    return render(request, 'pawns/pawn.html', {
        'pawn': pawn,
        'pawns': Pawn.objects.filter(parent=pawn)
    })

def new_pawn(request, slug=None):
    parent_pawn = None
    if slug:
        parent_pawn = get_object_or_404(Pawn, slug=slug)
        back_url = parent_pawn.url
    else:
        back_url = reverse('pawns')

    if request.method == 'POST':
        form = PawnForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                pawn = form.save(commit=False)
                pawn.user = request.user  
                if parent_pawn:
                    pawn.parent = parent_pawn
                pawn.save()
                messages.success(request, 'New pawn created!')
                return redirect(reverse('pawn', args=[pawn.slug]))
            except IntegrityError as e:
                form.fields['slug'].initial = form.cleaned_data['slug']
                if 'UNIQUE constraint failed' in str(e):
                    form.add_error('slug', f'{pawn.slug}: A pawn with this slug already exists.')
                else:
                    form.add_error(None, 'An error occurred while creating the pawn.')
    else:
        if parent_pawn:
            form = PawnForm(initial={'parent': parent_pawn})
        else:
            form = PawnForm()

    return render(request, 'pawns/form.html', {
        'form': form,
        'pawn': parent_pawn,
        'back_url': back_url
    })

def edit_pawn(request, slug):
    pawn = get_object_or_404(Pawn, slug=slug)

    if request.method == 'POST':
        form = PawnForm(request.POST, request.FILES, instance=pawn)
        if form.is_valid():
            form.save()
            messages.success(request, 'Pawn updated successfully!')
            return redirect(pawn.url())
    else:
        form = PawnForm(instance=pawn)
    return render(request, 'pawns/form.html', {
        'form': form,
        'pawn': pawn,
        'back_url': pawn.url
    })

def delete_pawn(request, slug):
    pawn = get_object_or_404(Pawn, slug=slug)
    if request.method == 'POST':
        url = pawn.parent_url()
        pawn.delete()
        return redirect(url)
    return render(request, 'ask.html', {
        'title': 'Delete Pawn',
        'text': f'You\'re deleting tha Pawn: <b>{pawn}</b>?',
        'url_back': pawn.url()
    })

def edit_questions(request, slug):
    pawn = get_object_or_404(Pawn, slug=slug)
    if request.method == 'POST':
        messages.success(request, 'Questions updated successfully!')
        questions_text = request.POST.get('questions').strip()
        pawn.questions.all().delete()
        for r in questions_text.split('.'):
            if not '?' in r: continue
            try:
                r = r.strip()
                t, a = r.split('?')
                c, a1, a2, a3 = a.split(';')
                Question.objects.create(pawn = pawn, user = request.user, text = t, correct = c, a1 = a1, a2 = a2, a3 = a3)
            except:
                messages.error(request, "error at: " + r)
        return redirect(pawn.url())
    return render(request, 'pawns/edit-questions.html', {
        'pawn': pawn
    })
