from django import forms
from .models import Pawn, Sentence, Question, OpenQuestion, OpenAnswer

class PawnForm(forms.ModelForm):
    class Meta:
        model = Pawn
        fields = ['is_public', 'name', 'text', 'parent', 'image', 'number', 'quiz', 'coze', 'partis', 'link', 'exam']  

class SentenceForm(forms.ModelForm):
    class Meta:
        model = Sentence
        fields = ['image', 'text', 'pawn']  

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['pawn', 'text', 'correct', 'a1', 'a2', 'a3']  

class OpenQuestionForm(forms.ModelForm):
    class Meta:
        model = OpenQuestion
        fields = ['text']

class OpenAnswerForm(forms.ModelForm):
    class Meta:
        model = OpenAnswer
        fields = ['openQuestion', 'text']

class QuestionsForm(forms.Form):
    text = forms.CharField(
        widget=forms.Textarea(
            attrs={'placeholder': 'questions?'}
        ),
        label='domanda??rispostagiusta;;rispostasbagliata;;rispostasbagliata;;rispostasbagliata..'
    )

    