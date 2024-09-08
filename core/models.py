import random, string
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.db import models
from django.contrib.auth.hashers import make_password

class User(AbstractUser):
    bio = models.TextField(null=True, blank=True)
    THEME_CHOICES = [
        ('red', 'Red'),
        ('blue', 'Blue'),
        ('green', 'Green'),
        ('yellow', 'Yellow'),
    ]
    theme = models.CharField(max_length=6, choices=THEME_CHOICES, default='blue')
    
    def url(self):
        return reverse('user', kwargs={'username': self.username})

    def url_delete(self):
        return reverse('user.delete', kwargs={'username': self.username})

    def url_reset(self):
        return reverse('user.reset', kwargs={'username': self.username})

    def pawns(self):
        from pawns.models import Pawn
        return Pawn.objects.filter(user=self, parent=None)

    def reset_password(self):
        new_password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        self.set_password(new_password) 
        self.save()
        return new_password

    def answer(self, question, state):
        from pawns.models import QuestionSubmitted
        a, _ = QuestionSubmitted.objects.get_or_create(question=question, user=self)
        if state:
            a.correctly += 1   
        else:
            a.wrongly += 1
        a.save()