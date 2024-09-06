from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from .models import User  # Import your custom User model

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
    users = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),  # Elenca tutti gli utenti disponibili
        widget=forms.CheckboxSelectMultiple,  # Usa una lista di checkbox per selezionare più utenti
        required=False  # Gli utenti possono essere rimossi tutti
    )

    class Meta:
        model = Group
        fields = []  # Non modifichiamo il nome del gruppo, solo i partecipanti

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            # Pre-compila il campo users con gli utenti attualmente associati al gruppo
            self.fields['users'].initial = self.instance.user_set.all()