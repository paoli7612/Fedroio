import random, re
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import Group
from django.utils.text import slugify
from django.urls import reverse
from django.db import models
from core.models import User

class Pawn(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    groups = models.ManyToManyField(Group, related_name='pawns', blank=True)  # Relazione con il modello Group
    slug = models.SlugField(max_length=512, unique=True, blank=True)
    name = models.CharField(max_length=128)
    text = models.TextField(max_length=512, null=True, blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='childs')
    image = models.ImageField(upload_to='pawn_images/', null=True, blank=True)  # Add this line
    number = models.PositiveIntegerField(null=True, blank=True)
    is_public = models.BooleanField(default=False)
    quiz = models.BooleanField(default=False)
    coze = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def url(self):
        return reverse('pawn', kwargs={'slug': self.slug})
    
    def users(self):
        return User.objects.filter(groups__in=self.groups.all()).distinct()

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
        parti = re.split(r'(\*.*?\*)', self.text)
        risultato = ['___' if part.startswith('*') and part.endswith('*') else part for part in parti]
        return risultato

    def __str__(self):
        return re.sub(r'\*(.*?)\*', r'<strong>\1</strong>', self.text)

    def control(self, dict):
        correct = {f'word_{i+1}': parola.strip('*') for i, parola in enumerate(self.text.split())}
        for k, w in dict.items():
            if w.lower() != correct[k].lower():
                return False
        return True

class Question(models.Model):
    pawn = models.ForeignKey(Pawn, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField(max_length=256)
    correct = models.CharField(max_length=128)
    a1 = models.CharField(max_length=128)
    a2 = models.CharField(max_length=128)
    a3 = models.CharField(max_length=128)

    def __str__(self):
        return self.text
    
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

    def delete_url(self):
        return reverse('question.delete', kwargs={'section_slug': self.section.slug, 'chapter_slug': self.chapter.slug, 'question_id': self.id})

    def userAnswered(self, user, state):
        if user.is_authenticated:
            user.answer(self, state)

class QuestionSubmitted(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='answers')
    correctly = models.IntegerField(default=0)
    wrongly = models.IntegerField(default=0)


