from django.db import models
from core.models import User

# Create your models here.

class Traccia(models.Model):
    text = models.TextField(max_length=4096)
    partis_run = models.BooleanField(default=False)

    def __str__(self):
        return self.text

class Tema(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='temi')
    traccia = models.ForeignKey(Traccia, on_delete=models.CASCADE, related_name='temi')
    text = models.TextField(max_length=4096)

    def __str__(self):
        return f"{self.user}__{self.traccia}__{self.text[:100]}"

class Griglia(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='griglie')
    tema = models.ForeignKey(Tema, on_delete=models.CASCADE, related_name='griglie')
    avreage = models.FloatField(null=True, blank=True)

    class Meta:
        unique_together = ('user', 'tema')

    def __str__(self):
        return f"{self.user}: {self.forma_ortografia} {self.forma_sintassi} {self.forma_semantica} {self.informazioni_sbagliate} {self.informazioni_in_eccesso} {self.informazioni_mancanti} {self.discorso_diretto} {self.figure_retoriche}"
    
    forma_ortografia = models.IntegerField(default=0, blank=True, null=True)
    forma_sintassi = models.IntegerField(default=0, blank=True, null=True)
    forma_semantica = models.IntegerField(default=0, blank=True, null=True)
    
    informazioni_sbagliate = models.IntegerField(default=0, blank=True, null=True)
    informazioni_in_eccesso = models.IntegerField(default=0, blank=True, null=True)
    informazioni_mancanti = models.IntegerField(default=0, blank=True, null=True)
    
    discorso_diretto = models.IntegerField(default=0, blank=True, null=True)
    figure_retoriche = models.IntegerField(default=0, blank=True, null=True)