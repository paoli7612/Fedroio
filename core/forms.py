from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm
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