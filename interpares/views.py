from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.messages import success
from django.contrib.auth.decorators import login_required
from .models import Tema

# Create your views here.
@login_required
def index(request):
    return render(request, 'interpares/index.html')

@login_required
def write(request):
    if request.method == 'POST':
        tema, _ = Tema.objects.get_or_create(user=request.user)
        tema.text = request.POST.get('text')
        tema.save()
        return redirect(reverse('interpares'))
    return render(request, 'interpares/write.html')

@login_required
def evaluate(request):
    tema = Tema.objects.exclude(user=request.user).order_by('?').first()
    if not tema:
        success(request, 'nessun tema da valutare')
        return redirect(reverse('account'))
    return render(request, 'interpares/evaluate.html', {
        'tema': tema
    })