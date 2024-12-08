from django import forms
from .models import Traccia, Tema, Griglia
from django.core.exceptions import NON_FIELD_ERRORS

class TracciaForm(forms.ModelForm):
    class Meta:
        model = Traccia
        fields = ['text']

class TemaForm(forms.ModelForm):
    class Meta:
        model = Tema
        fields = ['text']

class GrigliaForm(forms.ModelForm):
    class Meta:
        model = Griglia
        fields = [
            'forma_ortografia', 'forma_sintassi', 'forma_semantica',
            'informazioni_sbagliate', 'informazioni_in_eccesso', 'informazioni_mancanti',
            'discorso_diretto', 'figure_retoriche'
        ]