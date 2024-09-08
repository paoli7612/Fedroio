from django import forms
from .models import Pawn, Sentence, Question

class PawnForm(forms.ModelForm):
    class Meta:
        model = Pawn
        fields = ['is_public', 'name', 'text', 'parent', 'slug', 'image', 'number', 'quiz', 'coze', 'groups']  
    
class SentenceForm(forms.ModelForm):
    class Meta:
        model = Sentence
        fields = ['image', 'text', 'pawn']  

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['pawn', 'text', 'correct', 'a1', 'a2', 'a3']  


    