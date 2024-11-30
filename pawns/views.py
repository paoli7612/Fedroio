from django.shortcuts import render, get_object_or_404, redirect, get_list_or_404
from django.db import IntegrityError
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from .models import Pawn, Sentence, Question, OpenQuestion, OpenAnswer, JudgeQuestion
from .forms import PawnForm, SentenceForm, QuestionForm, QuestionsForm, OpenQuestionForm, OpenAnswerForm
from .views_exercise import *

def index(request):
    print(Pawn.objects.filter(parent=None, public=True).order_by('number'))
    return render(request, 'pawns/index.html', {
        'pawns': Pawn.objects.filter(parent=None, public=True).order_by('number'),
    })

def pawn(request, uuid):
    pawn = get_object_or_404(Pawn, uuid=uuid)
    if not pawn.public and not request.user == pawn.user:
        messages.error(request, 'Pawn not public')
    return render(request, 'pawns/pawn.html', {
        'pawn': pawn,
        'pawns': pawn.childs.order_by('number')
    })

def info_pawn(request, uuid):
    return render(request, 'pawns/info.html', {
        'pawn': get_object_or_404(Pawn, uuid=uuid)
    })

def new_pawn(request, uuid=None):
    parent_pawn = None
    if uuid:
        parent_pawn = get_object_or_404(Pawn, uuid=uuid)
        back_url = parent_pawn.url
    else:
        back_url = reverse('pawns')

    if request.method == 'POST':
        form = PawnForm(request.POST, request.FILES)
        if form.is_valid():
            pawn = form.save(commit=False)
            pawn.user = request.user  
            pawn.save()
            return redirect(pawn.url())
    else:
        if parent_pawn:
            form = PawnForm(initial={'parent': parent_pawn})
        else:
            form = PawnForm()

    return render(request, 'pawns/form.html', {
        'form': form,
        'pawn': parent_pawn,
        'back_url': back_url
    })

def edit_sentence(request, id):
    sentence = get_object_or_404(Sentence, id=id)
    if request.method == 'POST':
        form = SentenceForm(request.POST, request.FILES, instance=sentence)
        if form.is_valid():
            form.save()
            messages.success(request, 'Sentence updated successfully!')
            return redirect(sentence.pawn.url())
    else:
        form = SentenceForm(instance=sentence)
    return render(request, 'pawns/form.html', {
        'form': form,
        'back_url': sentence.pawn.url()
    })

def edit_question(request, id):
    quesiton = get_object_or_404(Question, id=id)
    if request.method == 'POST':
        form = QuestionForm(request.POST, request.FILES, instance=quesiton)
        if form.is_valid():
            form.save()
            messages.success(request, 'Sentence updated successfully!')
            return HttpResponseRedirect(request.POST.get('next'))
    else:
        form = QuestionForm(instance=quesiton)
    return render(request, 'pawns/form.html', {
        'form': form,
        'back_url': quesiton.pawn.url()
    })

def edit_openQuestion(request, id):
    openQuestion = get_object_or_404(OpenQuestion, id=id)
    if request.method == 'POST':
        form = OpenQuestionForm(request.POST, request.FILES, instance=openQuestion)
        if form.is_valid():
            form.save()
            messages.success(request, 'OpenQuestion updated successfully!')
            return HttpResponseRedirect(request.POST.get('next'))
    else:
        form = OpenQuestionForm(instance=openQuestion)
    return render(request, 'pawns/form.html', {
        'form': form,
        'back_url': openQuestion.pawn.url()
    })

def edit_pawn(request, uuid):
    pawn = get_object_or_404(Pawn, uuid=uuid)
    if request.method == 'POST':
        form = PawnForm(request.POST, request.FILES, instance=pawn)
        if form.is_valid():
            form.save()
            messages.success(request, 'Pawn updated successfully!')
            return redirect(pawn.url())
    else:
        form = PawnForm(instance=pawn)
    return render(request, 'pawns/form.html', {
        'form': form,
        'pawn': pawn,
        'back_url': pawn.url
    })

def delete_pawn(request, uuid):
    pawn = get_object_or_404(Pawn, uuid=uuid)
    if request.method == 'POST':
        url = pawn.parent_url()
        pawn.delete()
        return redirect(url)
    return render(request, 'ask.html', {
        'title': 'Delete Pawn',
        'text': f'You\'re deleting tha Pawn: <b>{pawn}</b>?',
        'url_back': pawn.url()
    })

def delete_question(request, id):
    question = get_object_or_404(Question, id=id)
    if request.method == 'POST':
        url = question.pawn.url()
        question.delete()
        return redirect(url)
    return render(request, 'ask.html', {
        'title': 'Delete Question',
        'text': f'You\'re deleting the Question: <b>{question}</b>?',
        'url_back': question.pawn.url()
    })

def delete_openQuestion(request, id):
    openQuestion = get_object_or_404(OpenQuestion, id=id)
    if request.method == 'POST':
        url = openQuestion.pawn.url()
        openQuestion.delete()
        return redirect(url)
    return render(request, 'ask.html', {
        'title': 'Delete openQuestion',
        'text': f'You\'re deleting the openQuestion: <b>{openQuestion}</b>?',
        'url_back': openQuestion.pawn.url()
    })

def delete_sentence(request, id):
    sentence = get_object_or_404(Sentence, id=id)
    if request.method == 'POST':
        url = sentence.pawn.url()
        sentence.delete()
        return redirect(url)
    return render(request, 'ask.html', {
        'title': 'Delete sentence',
        'text': f'You\'re deleting this sentence: <b>{sentence}</b>?',
        'url_back': sentence.pawn.url()
    })

def new_sentence(request, uuid):
    pawn = get_object_or_404(Pawn, uuid=uuid)
    if request.method == 'POST':
        form = SentenceForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'New sentence created!')
            return redirect(reverse('pawn', kwargs={'uuid': pawn.uuid}))
    else:
        form = SentenceForm(initial={'pawn': pawn})

    return render(request, 'pawns/form.html', {
        'form': form,
        'pawn': pawn,
        'back_url': pawn.url()
    })

def new_question(request, uuid):
    pawn = get_object_or_404(Pawn, uuid=uuid)
    if request.method == 'POST':
        form = QuestionForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'New sentence created!')
            return redirect(reverse('pawn', kwargs={'uuid': pawn.uuid}))
    else:
        form = QuestionForm(initial={'pawn': pawn})

    return render(request, 'pawns/form.html', {
        'form': form,
        'pawn': pawn,
        'back_url': pawn.url()
    })

def new_questions(request, uuid):
    pawn = get_object_or_404(Pawn, uuid=uuid)
    if request.method == 'POST':
        form = QuestionsForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['text']
            errors = pawn.newQuestions_byText(text)
            if errors:
                messages.error(request, errors)
            return redirect(pawn.url())
    else:
        form = QuestionsForm()

    return render(request, 'pawns/form.html', {
        'form': form,
        'pawn': pawn,
        'back_url': pawn.url()
    })

def new_openQuestion(request, uuid):
    pawn = get_object_or_404(Pawn, uuid=uuid)
    if request.method == 'POST':
        print(request.POST)
        openQuestion = OpenQuestion.objects.create(text=request.POST.get('text'), pawn=pawn)
        return redirect(pawn.url())
    else:
        form = OpenQuestionForm()

    return render(request, 'pawns/form.html', {
        'form': form,
        'pawn': pawn,
        'back_url': pawn.url()
    })

def exam(request, uuid, mode='normal'):
    pawn = get_object_or_404(Pawn, uuid=uuid)
    if mode == 'normal':
        questions = pawn.all_questions(isRandom=True)[:pawn.exam_count]
    elif mode == 'hard':
        questions = pawn.worst_questions()[:pawn.exam_count]
    time = pawn.exam_time

    if request.method == 'POST':
        questions = list()
        for k, v in request.POST.items():
            try:
                id = int(k)
                question = get_object_or_404(Question, id=id)
                question.slected = int(v)
                questions.append(question)
            except: pass
        return render(request, 'pawns/exam-result.html', {
            'questions': questions,
            'time': request.POST.get('time')
        })
    
    return render(request, 'pawns/exam.html', {
        'questions': questions,
        'time': time
    })

@login_required
def partis(request, id):
    question = get_object_or_404(OpenQuestion, id=id)
    try:
        open_answer = OpenAnswer.objects.get(user=request.user, openQuestion=question)
    except OpenAnswer.DoesNotExist:
        open_answer = OpenAnswer()
        open_answer.openQuestion = question

    if request.method == 'POST':
        form = OpenAnswerForm(request.POST, instance=open_answer)
        if form.is_valid():
            open_answer = form.save(commit=False)
            open_answer.user = request.user
            open_answer.openQuestion = question  # Associa la risposta alla domanda
            open_answer.save()
            return redirect(question.pawn.url())
    else:
        
        form = OpenAnswerForm(instance=open_answer)

    return render(request, 'pawns/form.html', {
        'form': form,
        'pawn': question.pawn,  # Usa la relazione dalla domanda per ottenere il pawn
        'back_url': question.pawn.url(),
    })

def openQuestion_answers(request, id):
    return render(request, 'partis/answers.html', {
        'openQuestion': get_object_or_404(OpenQuestion, id=id)
    })

def answer_delete(request, id):
    openAnswer = get_object_or_404(OpenAnswer, id=id)
    if request.method == 'POST':
        openAnswer.delete()
        return redirect(reverse('account'))
    return render(request, 'ask.html', {
        'title': 'Delete Pawn',
        'text': f'You\'re deleting that answer?: <b>{openAnswer}</b>?',
        'url_back': openAnswer.openQuestion.pawn.url()
    })

def openQuestion_eye(request, id):
    openQuestion = get_object_or_404(OpenQuestion, id=id)
    pawn = openQuestion.pawn
    if request.method == 'POST':
        for k, v in request.POST.items():
            if 'answer' == k[:6]:
                answer_id = k.split('answer')[1]
                answer = get_object_or_404(OpenAnswer, id=answer_id)
                jq, _ = JudgeQuestion.objects.update_or_create(openAnswer=answer, user=request.user)
                jq.value = v
                jq.save()
        return redirect(pawn.url())

    return render(request, 'pawns/eyeOpenQuestion.html', {
        'openQuestion': openQuestion
    })