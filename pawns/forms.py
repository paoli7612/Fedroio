from django import forms
from .models import Pawn

class PawnForm(forms.ModelForm):
    class Meta:
        model = Pawn
        fields = ['image', 'number', 'name', 'text', 'parent', 'slug']  


