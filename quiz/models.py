import random
from pawns.models import Pawn
from django.shortcuts import get_object_or_404
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

from django.db import models

# Create your models here.
class Question(models.Model):
    pawn = models.ForeignKey(Pawn, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField(max_length=256)
    correct = models.CharField(max_length=128)
    a1 = models.CharField(max_length=128)
    a2 = models.CharField(max_length=128)
    a3 = models.CharField(max_length=128)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.text
    
    def to_str(self):
        return f"{self.text};{self.correct};{self.a1};{self.a2};{self.a3}."

    def get_random_answers(self):
        answers = list(enumerate([self.correct, self.a1, self.a2, self.a3]))
        random.shuffle(answers)
        return answers

    def delete_url(self):
        return reverse('question.delete', kwargs={'section_slug': self.section.slug, 'chapter_slug': self.chapter.slug, 'question_id': self.id})

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='answers')
    state = models.BooleanField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} answered "{self.question.text}" on {self.date} ' + ('correctly' if self.state else 'wrongly')
