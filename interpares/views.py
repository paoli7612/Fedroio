from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.messages import success
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

from .forms import TracciaForm, TemaForm, GrigliaForm
from .models import Tema, Traccia, Griglia

# Create your views here.
@login_required
def index(request):
    if request.method == 'POST':
        traccia = get_object_or_404(Traccia, id=request.POST.get('traccia_id'))
        if traccia.partis_run:
            traccia.partis_run = False
        else:
            traccia.partis_run = True
        traccia.save()
        return redirect(reverse('interpares'))
    return render(request, 'interpares/index.html', {
        'tracce': Traccia.objects.all(),
        'groups': Group.objects.all(),
    })

@login_required
def write(request, id):
    traccia = get_object_or_404(Traccia, id=id)
    tema, created = Tema.objects.get_or_create(user=request.user, traccia=traccia) 

    if request.method == 'POST':
        form = TemaForm(request.POST, instance=tema) 
        if form.is_valid():
            form.save() 
            return redirect(reverse('interpares'))
    else:
       
        form = TemaForm(instance=tema)

    return render(request, 'interpares/form.html', {
        'form': form,
        'back_url': reverse('interpares')
    })

@login_required
def evaluate(request, id=None):
    if id:
        tema = get_object_or_404(Tema, id=id)
    else:
        tema = Tema.objects.filter(griglie__isnull=True).exclude(user=request.user).order_by('?').first()
        if not tema:
            messages.success(request, 'nessun tema da valutare')
            return redirect(reverse('account'))
        return redirect(reverse('interpares.evaluate', kwargs={'id': tema.id}))
    if request.method == 'POST':
        form = GrigliaForm(request.POST)
        if form.is_valid():
            griglia = form.save(commit=False) 
            griglia.user = request.user      
            griglia.tema = tema              
            griglia.save()                   
            return redirect(reverse('interpares'))
    else:
        form = GrigliaForm()

    return render(request, 'interpares/evaluate.html', {
        'tema': tema,
        'form': form
    })

@login_required
def newTraccia(request):
    if request.method == 'POST':
        form = TracciaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('interpares'))
    else:
        form = TracciaForm()

    return render(request, 'interpares/form.html', {
        'form': form,
        'back_url': reverse('interpares')
    })

@login_required
def deleteTraccia(request, id):
    traccia = get_object_or_404(Traccia, id=id)
    if request.method == 'POST':
        traccia.delete()
        return  redirect(reverse('interpares'))
    return render(request, 'ask.html', {
        'title': 'Delete Traccia',
        'text': f'You\'re deleting the Traccia: <b>{traccia}</b>?',
        'url_back': reverse('interpares')
    })