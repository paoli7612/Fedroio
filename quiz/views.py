from django.db.models import Case, When
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib import messages
from random import choice, shuffle

from .models import Question, Answer
from .forms import QuestionForm

from pawns.models import Pawn

def index(request):
    return render(request, 'quiz/index.html')

def question_edit(request, id):
    question = get_object_or_404(Question, id=id)

    if request.method == 'POST':
        form = QuestionForm(request.POST, request.FILES, instance=question)
        if form.is_valid():
            form.save()
            messages.success(request, 'question updated successfully!')
    else:
        form = QuestionForm(instance=question)
    return render(request, 'pawns/form.html', {
        'form': form,
        'back_url': question.pawn.url
    })

def question_new(request, slug):
    pawn = get_object_or_404(Pawn, slug=slug)

    if request.method == 'POST':
        form = QuestionForm(request.POST, request.FILES)
        if form.is_valid():
            question = form.save(commit=False)
            question.pawn = pawn
            question.save()
            messages.success(request, 'question created successfully!')
    else:
        form = QuestionForm()
    return render(request, 'pawns/form.html', {
        'form': form,
        'back_url': pawn.url
    })

def question_delete(request, id):
    question = get_object_or_404(Question, id=id)
    if request.method == 'POST':
        url = question.pawn.url()
        question.delete()
        return redirect(url)
    return render(request, 'ask.html', {
        'title': 'Delete question',
        'text': f'You\'re deleting tha question: <b>{question}</b>?',
        'url_back': question.pawn.url()
    })

def points(request, pawn_slug):
    pawn = get_object_or_404(Pawn, slug=pawn_slug)
    questions = pawn.all_questions() # prendo tutte le domande di questo pawns o i figli
    if request.method == 'GET': # Nuova partita
        request.session['points'] = 0
        request.session['answered_questions'] = [] 
        question = choice(questions)
    else: # Risposta ad una domanda
        question_id = request.POST.get('id')
        question = get_object_or_404(Question, id=question_id)

        if request.POST.get('answer') == '0': # Se ha risposto correttamente

            if question_id in request.session['answered_questions']: # Se è gia stata risposta questa domanda durante questa partita riavvia la partita (probabile abuso della applicazione)
                messages.error(request, 'Hai già risposto a questa domanda!')
                return redirect(reverse('quiz.points', kwargs={'pawn_slug': pawn_slug}))
            else: # non dovrebbe avere imbrogliato
                request.session['points'] += 1 # un punto nella session
                messages.success(request, 'Corretto') # messaggio "corretto"
                question.userAnswered(request.user, True)

                request.session['answered_questions'].append(question_id)
                
                questions_filtered = [question for question in questions if str(question.id) not in request.session['answered_questions']] # prendo le domande che non ho ancora risposto
                if len(questions_filtered) == 0: # se le domande sono finite
                    messages.success(request, 'Risposte completate :D')
                    return redirect(reverse('account'))
                else: # se ci sono ancora domande
                    question = choice(questions_filtered)
        else: # Se la risposta non è corretta
            if request.user.is_authenticated:
                request.user.answer(question, False)

            messages.error(request, 'Errore')

    return render(request, 'quiz/points.html', {
        'points': request.session['points'],
        'question': question
    })

def chain(request, pawn_slug):
    pawn = get_object_or_404(Pawn, slug=pawn_slug)
    questions = pawn.all_questions()
    if request.method == 'GET':
        nextQuestion = choice(questions)
        chain = [nextQuestion]
        request.session['chain'] = [chain[0].id]
        request.session['points'] = 0
    else:
        question = get_object_or_404(Question, id=request.POST.get('id'))
        chain_ids = request.session['chain']
        order = Case(*[When(id=pk, then=pos) for pos, pk in enumerate(chain_ids)])
        chain = list(Question.objects.filter(id__in=chain_ids).order_by(order))
        if request.POST.get('answer') == '0':
            question.userAnswered(request.user, True)
            request.session['points'] += 1
            if len(chain) == request.session['points']:
                questions_filtered = [question for question in questions if question not in chain] # prendo le domande che non ho ancora messo in chain
                if len(questions_filtered) == 0:
                    messages.success(request, 'Risposte completate :D')
                    return redirect(reverse('account'))
                nextQuestion = choice(questions_filtered)
                request.session['chain'].append(nextQuestion.id)
                chain.append(nextQuestion)
            else:
                nextQuestion = get_object_or_404(Question, id=request.session['chain'][request.session['points']])
        else:
            question.userAnswered(request.user, False)
            request.session['points'] = 0
            nextQuestion = chain[0]
        
    return render(request, 'quiz/chain.html', {
        'points': request.session['points'],
        'question': nextQuestion,
        'questions': chain
    })