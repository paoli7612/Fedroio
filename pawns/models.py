import random, re, uuid
import uuid
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import Group
from django.utils.text import slugify
from django.urls import reverse
from django.db import models
from core.models import User

class Pawn(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='childs')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    groups = models.ManyToManyField(Group, related_name='pawns', blank=True)  # Relazione con il modello Group

    number = models.PositiveIntegerField(null=True, blank=True)
    name = models.CharField(max_length=128)
    text = models.TextField(max_length=512, null=True, blank=True)
    image = models.ImageField(upload_to='pawn_images/', null=True, blank=True)  # Add this line
    
    is_public = models.BooleanField(default=False)
    quiz = models.BooleanField(default=False)
    coze = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def url(self):
        return reverse('pawn', kwargs={'uuid': self.uuid})

    def url_new(self):
        return reverse('pawn.new', kwargs={'uuid': self.uuid})
    
    def url_delete(self):
        return reverse('pawn.delete', kwargs={'uuid': self.uuid})

    def url_edit(self):
        return reverse('pawn.edit', kwargs={'uuid': self.uuid})

    def url_newQuestion(self):
        return reverse('pawn.question-new', kwargs={'uuid': self.uuid})

    def url_newQuestions(self):
        return reverse('pawn.questions-new', kwargs={'uuid': self.uuid})

    def url_newSentence(self):
        return reverse('pawn.sentence-new', kwargs={'uuid': self.uuid})

    def url_quizPoints(self):
        return reverse('pawn.quiz-points', kwargs={'uuid': self.uuid})
    
    def url_quizChain(self):
        return reverse('pawn.quiz-chain', kwargs={'uuid': self.uuid})

    def url_cozePlay(self):
        return reverse('pawn.coze', kwargs={'uuid': self.uuid})
        
    def url_cozeChoice(self):
        return reverse('pawn.coze-choice', kwargs={'uuid': self.uuid})

    def users(self):
        return User.objects.filter(groups__in=self.groups.all()).distinct()

    def newQuestions_byText(self, text):
        errors = str()
        for q in text.split('..'):
            try:
                q.strip()
                if not q: continue
                text, answers = q.split('??')
                correct, a1, a2, a3 = answers.split(';;')
                Question.objects.create(
                    pawn = self,
                    text = text,
                    correct = correct,
                    a1 = a1, a2 = a2, a3 = a3
                )
            except:
                errors += q


    def parent_url(self):
        if self.parent:
            return self.parent.url()
        else:
            return reverse('pawns')
        
    def breadcrumb(self):
        if self.parent:
            return self.parent.breadcrumb() + [self]
        else:
            return [self]
        
    def all_questions(self):
        questions = list(self.questions.all())
        for child in self.childs.all():
            questions_child = child.all_questions()
            if questions_child:
                questions += questions_child
        return questions
    
    def all_sentences(self):
        sentences = list(self.sentences.all())
        for child in self.childs.all():
            sentences_child = child.all_sentences()
            if sentences_child:
                sentences += sentences_child
        random.shuffle(sentences)
        return sentences
    
    def all_words(self):
        sentences = self.all_sentences()
        words = list()
        for s in sentences:
            for w in s.text.split(' '):
                if w[0] == w[-1] == '*':
                    words.append(w[1:-1])
        random.shuffle(words)
        return words

class Sentence(models.Model):
    pawn = models.ForeignKey(Pawn, on_delete=models.CASCADE, related_name='sentences')
    text = models.TextField(max_length=512)
    image = models.ImageField(null=True, blank=True)

    def words(self):
        return re.findall(r'\*(.*?)\*', self.text)

    def url_edit(self):
        return reverse('pawns.sentence-edit', kwargs={'id': self.id})

    def url_delete(self):
        return reverse('pawns.sentence-delete', kwargs={'id': self.id})

    def hide_words(self):
        return ['___' if part.startswith('*') and part.endswith('*') else part for part in re.split(r'(\*.*?\*)', self.text)]

    def __str__(self):
        return re.sub(r'\*(.*?)\*', r'<strong>\1</strong>', self.text)

    def control(self, words):
        final = list()
        result = True
        corrects = [word.lower().strip() for word in self.words()]  
        for word in words:
            if not word.lower() in corrects:
                result = False
            final.append(word)
        return final, result

class Question(models.Model):
    pawn = models.ForeignKey(Pawn, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField(max_length=256)
    correct = models.CharField(max_length=128)
    a1 = models.CharField(max_length=128)
    a2 = models.CharField(max_length=128)
    a3 = models.CharField(max_length=128)

    def __str__(self):
        return self.text
    
    def error(self):
        dif = abs(len(self.correct) - max(map(len, [self.a1, self.a2, self.a3])))
        return dif > len(self.correct)/10

    def url_edit(self):
        return reverse('pawns.question-edit', kwargs={'id': self.id})

    def url_delete(self):
        return reverse('pawns.question-delete', kwargs={'id': self.id})

    def to_str(self):
        return f"{self.text};{self.correct};{self.a1};{self.a2};{self.a3}."

    def get_random_answers(self):
        answers = list(enumerate([self.correct, self.a1, self.a2, self.a3]))
        random.shuffle(answers)
        return answers

    def userAnswered(self, user, state):
        if user.is_authenticated:
            user.answer(self, state)

class QuestionSubmitted(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='answers')
    correctly = models.IntegerField(default=0)
    wrongly = models.IntegerField(default=0)


