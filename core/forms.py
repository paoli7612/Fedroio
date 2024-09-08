from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from .models import User  # Import your custom User model

class SettingsForm(forms.Form):
    class Meta:
        model = User
        fields = ['theme']
        widgets = {
            'theme': forms.RadioSelect(choices=[('dark', 'Dark Theme'), ('light', 'Light Theme')]),
        }
    theme = forms.ChoiceField(choices=[
        ('blue', 'Blue'),
        ('red', 'Red'),
        ('green', 'Green'),
        ('yellow', 'Yellow')
    ])

class UserForm(UserCreationForm):
    usable_password = None
    email = forms.EmailField(required=True, help_text="Enter a valid email address.")

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = ""
        user.last_name = ""
        user.bio = ""
        if commit:
            user.save()
        return user
    
class GroupMembersForm(forms.ModelForm):
    name = forms.CharField(label="Nome del gruppo", max_length=150)
    users = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),  # Elenca tutti gli utenti disponibili
        widget=forms.CheckboxSelectMultiple,  # Usa una lista di checkbox per selezionare più utenti
        required=False  # Gli utenti possono essere rimossi tutti
    )

    class Meta:
        model = Group
        fields = ['name']  # Includiamo il campo 'name' del gruppo e i membri

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            # Se è un gruppo esistente, pre-compila gli utenti associati
            self.fields['users'].initial = self.instance.user_set.all()

    def save(self, commit=True):
        # Salva prima il gruppo, che include il nome
        group = super().save(commit=False)
        
        if commit:
            group.save()
        
        # Aggiorna i membri del gruppo (gli utenti selezionati)
        if self.cleaned_data['users']:
            group.user_set.set(self.cleaned_data['users'])
        
        return group