from django import forms
from .models import Pawn, Sentence, Question

class PawnForm(forms.ModelForm):
    class Meta:
        model = Pawn
        fields = ['is_public', 'name', 'text', 'parent', 'image', 'number', 'quiz', 'coze', 'link']  

class SentenceForm(forms.ModelForm):
    class Meta:
        model = Sentence
        fields = ['image', 'text', 'pawn']  

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['pawn', 'text', 'correct', 'a1', 'a2', 'a3']  

class QuestionsForm(forms.Form):
    text = forms.CharField(
        widget=forms.Textarea(
            attrs={'placeholder': 'questions?'}
        ),
        label='domanda??rispostagiusta;;rispostasbagliata;;rispostasbagliata;;rispostasbagliata..'
    )

    