from django.db import models
from core.models import User

# Create your models here.

class Traccia(models.Model):
    text = models.TextField

class Tema(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='temi')
    text = models.TextField(max_length=4096)

class Griglia(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='griglie')
    tema = models.ForeignKey(Tema, on_delete=models.CASCADE, related_name='griglie')
    
    forma_ortografia = models.IntegerField(default=0, blank=True, null=True)
    forma_sintassi = models.IntegerField(default=0, blank=True, null=True)
    forma_semantica = models.IntegerField(default=0, blank=True, null=True)
    
    informazioni_sbagliate = models.IntegerField(default=0, blank=True, null=True)
    informazioni_in_eccesso = models.IntegerField(default=0, blank=True, null=True)
    informazioni_mancanti = models.IntegerField(default=0, blank=True, null=True)
    
    discorso_diretto = models.IntegerField(default=0, blank=True, null=True)
    figure_retoriche = models.IntegerField(default=0, blank=True, null=True)