import random, re, uuid
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import Group
from django.urls import reverse
from django.db import models
from core.models import User

class Pawn(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='childs') 
    
    user = models.ForeignKey(User, on_delete=models.CASCADE) # utente creatore
    editors = models.ManyToManyField(User, related_name='editablePawns', blank=True) # grouppo che può modificare questo pawn
    groups = models.ManyToManyField(Group, related_name='pawns', blank=True) # grouppi che possono modificarlo
    number = models.PositiveIntegerField(null=True, blank=True) # numero tra i fratelli
    name = models.CharField(max_length=128) # titolo 
    text = models.TextField(max_length=512, null=True, blank=True) # testo contenuto
    image = models.ImageField(upload_to='pawn_images/', null=True, blank=True)  # immagine contenuta
    link = models.TextField(max_length=256, blank=True, null=True) # link a risorsa esterna
    
    public = models.BooleanField(default=False) # show in public?
    active = models.BooleanField(default=False) # show in active?
    explore = models.BooleanField(default=False) # allow to explore
    quiz = models.BooleanField(default=False) # allow quiz game
    coze = models.BooleanField(default=False) # allow coze game
    exam = models.BooleanField(default=False) # allow doing esam
    partis = models.BooleanField(default=False) # allow open question

    partis_run = models.BooleanField(default=False) # mode to allow autoevaluate users
    exam_count = models.IntegerField(default=36) # count of question for exam
    exam_time = models.IntegerField(default=45) # minutes for each exam

    def __str__(self):
        return self.name
    
    def url(self): return reverse('pawn', kwargs={'uuid': self.uuid})
    def url_edit(self): return reverse('pawn.edit', kwargs={'uuid': self.uuid})
    def url_delete(self): return reverse('pawn.delete', kwargs={'uuid': self.uuid})
    def url_new(self): return reverse('pawn.new', kwargs={'uuid': self.uuid})
    def url_info(self): return reverse('pawn.info', kwargs={'uuid': self.uuid})

    def url_newSentence(self): return reverse('pawn.sentence-new', kwargs={'uuid': self.uuid})
    def url_newQuestion(self): return reverse('pawn.question-new', kwargs={'uuid': self.uuid})
    def url_newQuestions(self): return reverse('pawn.questions-new', kwargs={'uuid': self.uuid})
    def url_newOpenQuestion(self): return reverse('pawn.openQuestion-new', kwargs={'uuid': self.uuid})

    def url_quizPoints(self): return reverse('pawn.quiz-points', kwargs={'uuid': self.uuid})
    def url_quizHard(self): return reverse('pawn.quiz-pointsHard', kwargs={'uuid': self.uuid})
    def url_quizChain(self): return reverse('pawn.quiz-chain', kwargs={'uuid': self.uuid})
    def url_cozeEasy(self): return reverse('pawn.coze', kwargs={'uuid': self.uuid, 'difficulty': 1})
    def url_cozeNormal(self): return reverse('pawn.coze', kwargs={'uuid': self.uuid, 'difficulty': 2})
    def url_cozeHard(self): return reverse('pawn.coze', kwargs={'uuid': self.uuid, 'difficulty': 3})
    def url_cozeChoice(self): return reverse('pawn.coze-choice', kwargs={'uuid': self.uuid})

    def url_exam(self): return reverse('pawn.exam', kwargs={'uuid': self.uuid})
    def url_examPlus(self): return reverse('pawn.examPlus', kwargs={'uuid': self.uuid, 'mode': 'hard'})
    def url_explore(self): return reverse('explore', kwargs={'uuid': self.uuid})
    
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
            except Exception as e:
                print(e)
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
        
    def has_children(self):
        if self.childs.all().count()>0:
            return 1
        else:
            return 0

    def childs_explore(self):
        return self.childs.filter(explore=True)
 
    def all_questions(self, isRandom=False):
        questions = list(self.questions.all())
        for child in self.childs.all():
            questions_child = child.all_questions()
            if questions_child:
                questions += questions_child
        if isRandom:
            random.shuffle(questions)
        return questions
    
    def all_openQuestions(self, isRandom=False):
        questions = list(self.openQuestions.all())
        for child in self.childs.all():
            questions_child = child.all_openQuestions()
            if questions_child:
                questions += questions_child
        if isRandom:
            random.shuffle(questions)
        return questions
    
    def worst_questions(self):
        questions = self.all_questions()
        questions = sorted(
            questions,
            key=lambda q: (q.correctly + q.wrongly)/q.wrongly if q.wrongly != 0 else float('inf')  # float('inf') sposta le domande con wrongly=0 in fondo
        )
        return questions[:10]  # Prendi le 10 peggiori
    
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

class OpenQuestion(models.Model):
    pawn = models.ForeignKey(Pawn, on_delete=models.CASCADE, related_name='openQuestions')
    text = models.TextField(max_length=512, blank=False)
    correctAnswer = models.TextField(max_length=512, blank=True)

    def url_edit(self):
        return reverse('pawns.openQuestion-edit', kwargs={'id': self.id})

    def url_delete(self):
        return reverse('pawns.openQuestion-delete', kwargs={'id': self.id})

    def url_answers(self):
        return reverse('pawns.openQuestion-answers', kwargs={'id': self.id})

    def url_answer(self):
        return reverse('openAnswer.new', kwargs={'id': self.id})  

    def url_eye(self):
        return reverse('openQuestion.eye', kwargs={'id': self.id})

    def __str__(self):
        return self.text

class OpenAnswer(models.Model):
    openQuestion = models.ForeignKey(OpenQuestion, on_delete=models.CASCADE, related_name='answers')
    text = models.TextField(max_length=1024, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='answers')
    group = models.ForeignKey(Group, null=True, on_delete=models.SET_NULL)
    freeze = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'openQuestion')

    def url_edit(self):
        return reverse('openAnswer.new', kwargs={'id': self.openQuestion.id})     

    def url_delete(self):
        return reverse('openAnswer.delete', kwargs={'id': self.id})

class JudgeQuestion(models.Model):
    openAnswer = models.ForeignKey(OpenAnswer, on_delete=models.CASCADE, related_name='judges')
    value = models.IntegerField(default=5)
    note = models.TextField(max_length=512)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='judgeAnswers')

    def __str__(self):
        return str(self.value)

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
        corrects = [word.lower().strip() for word in self.words()]  
        for word in words:
            if word.lower() in corrects:
                final.append(word)
        return final

class Question(models.Model):
    pawn = models.ForeignKey(Pawn, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField(max_length=256)
    correct = models.CharField(max_length=128)
    a1 = models.CharField(max_length=128)
    a2 = models.CharField(max_length=128)
    a3 = models.CharField(max_length=128)
    wrongly = models.PositiveIntegerField(default=0)
    correctly = models.PositiveIntegerField(default=0)

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
    
    def error(self):
        dif = len(self.correct) - max(map(len, [self.a1, self.a2, self.a3]))
        return dif > len(self.correct)/4
    
    def answer(self, result):
        if result:
            self.correctly += 1
        else:
            self.wrongly += 1
        self.save()

    def correctness(self):
        try:
            return round((self.correctly / (self.correctly + self.wrongly)) * 100)
        except ZeroDivisionError:
            return 100
