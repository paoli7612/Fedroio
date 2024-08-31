from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    bio = models.TextField(null=True, blank=True)

    def answer(self, question, state):
        from quiz.models import Answer
        a, _ = Answer.objects.get_or_create(question=question, user=self)
        if state:
            a.correctly += 1   
        else:
            a.wrongly += 1
        a.save()