from django import forms
from .models import Pawn, Sentence, Question, OpenQuestion, OpenAnswer

class PawnForm(forms.ModelForm):
    class Meta:
        model = Pawn
        fields = ['is_public', 'hide', 'name', 'text', 'parent', 'image', 'number', 'quiz', 'coze', 'partis', 'link', 'exam', 'exam_count', 'groups']  

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
        fields = ['text', 'correctAnswer']

class OpenAnswerForm(forms.ModelForm):
    question_text = forms.CharField(
        label="Domanda",
        required=False,
        widget=forms.TextInput(attrs={'readonly': 'readonly'}),
    )

    class Meta:
        model = OpenAnswer
        fields = ['question_text', 'text', 'openQuestion']  # Aggiungi il campo visibile

        widgets = {
            'openQuestion': forms.HiddenInput(),  # Campo nascosto
        }
        labels = {
            'openQuestion': '',  # Rimuove la label
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.openQuestion:
            self.fields['question_text'].initial = self.instance.openQuestion.text

class QuestionsForm(forms.Form):
    text = forms.CharField(
        widget=forms.Textarea(
            attrs={'placeholder': 'questions?'}
        ),
        label='domanda??rispostagiusta;;rispostasbagliata;;rispostasbagliata;;rispostasbagliata..'
    )

    