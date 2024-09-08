import random
from django.db.models import Case, When 
from django.shortcuts import render, get_object_or_404, redirect
from django.db import IntegrityError
from django.urls import reverse
from django.contrib import messages
from .models import Pawn, Sentence, Question
from .forms import PawnForm, SentenceForm, QuestionForm

def index(request):
    return render(request, 'pawns/index.html', {
        'pawns': Pawn.objects.filter(parent=None, is_public=True),
    })

def pawn(request, uuid):
    pawn = get_object_or_404(Pawn, uuid=uuid)
    return render(request, 'pawns/pawn.html', {
        'pawn': pawn
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
            try:
                pawn = form.save(commit=False)
                pawn.user = request.user  
                if parent_pawn:
                    pawn.parent = parent_pawn
                pawn.save()
                messages.success(request, 'New pawn created!')
                return redirect(reverse('pawn', kwargs={'uuid': pawn.uuid}))
            except IntegrityError as e:
                form.add_error(None, 'An error occurred while creating the pawn.')
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
            return redirect(quesiton.pawn.url())
    else:
        form = QuestionForm(instance=quesiton)
    return render(request, 'pawns/form.html', {
        'form': form,
        'back_url': quesiton.pawn.url()
    })

def edit_pawn(request, uuid):
    pawn = get_object_or_404(Pawn, uuid=uuid)
    print(pawn.user)
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

def quiz_points(request, uuid):
    pawn = get_object_or_404(Pawn, uuid=uuid)
    questions = pawn.all_questions() # prendo tutte le domande di questo pawns o i figli
    if request.method == 'GET': # Nuova partita
        request.session['points'] = 0
        request.session['answered_questions'] = [] 
        question = random.choice(questions)
    else: # Risposta ad una domanda
        question_id = request.POST.get('id')
        question = get_object_or_404(Question, id=question_id)

        if request.POST.get('answer') == '0': # Se ha risposto correttamente

            if question_id in request.session['answered_questions']: # Se è gia stata risposta questa domanda durante questa partita riavvia la partita (probabile abuso della applicazione)
                messages.error(request, 'Hai già risposto a questa domanda!')
                return redirect(reverse('pawn.quiz-points', kwargs={'uuid': uuid}))
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
                    question = random.choice(questions_filtered)
        else: # Se la risposta non è corretta
            if request.user.is_authenticated:
                request.user.answer(question, False)

            messages.error(request, 'Errore')

    return render(request, 'quiz/points.html', {
        'points': request.session['points'],
        'question': question
    })

def quiz_chain(request, uuid):
    pawn = get_object_or_404(Pawn, uuid=uuid)
    questions = pawn.all_questions()

    if request.method == 'GET':
        nextQuestion = random.choice(questions)
        chain = [nextQuestion]
        request.session['chain'] = [chain[0].id]
        request.session['points'] = 0
    else:
        question = get_object_or_404(Question, id=request.POST.get('id'))
        chain_ids = request.session['chain']
        order = Case(*[When(id=pk, then=pos) for pos, pk in enumerate(chain_ids)])
        chain = list(Question.objects.filter(id__in=chain_ids).order_by(order))
        if request.POST.get('answer') == '0':
            messages.success(request, 'Corretto') # messaggio "corretto"
            question.userAnswered(request.user, True)
            request.session['points'] += 1
            if len(chain) == request.session['points']:
                questions_filtered = [question for question in questions if question not in chain] # prendo le domande che non ho ancora messo in chain
                if len(questions_filtered) == 0:
                    messages.success(request, 'Risposte completate :D')
                    return redirect(reverse('account'))
                nextQuestion = random.choice(questions_filtered)
                request.session['chain'].append(nextQuestion.id)
                chain.append(nextQuestion)
            else:
                nextQuestion = get_object_or_404(Question, id=request.session['chain'][request.session['points']])
        else:
            messages.error(request, 'Errore')
            question.userAnswered(request.user, False)
            request.session['points'] = 0
            nextQuestion = chain[0]
        
    return render(request, 'quiz/chain.html', {
        'points': request.session['points']+1,
        'question': nextQuestion,
        'questions': chain
    })

def coze(request, uuid, difficulty=4):
    pawn = get_object_or_404(Pawn, uuid=uuid)

    if request.method == 'POST':
        sentence = get_object_or_404(Sentence, id=int(request.POST.get('sentence_id')))
        input_words = request.POST.getlist('words[]')
        corrects, result = sentence.control(input_words)
        if result:
            messages.success(request, 'Corretto')
            sentence = random.choice(pawn.all_sentences())
            corrects = list()
        else:
            messages.error(request, 'Riprova' + str(corrects))
    else:
        sentence = random.choice(pawn.all_sentences())
        corrects = list()

    options = set()
    words = pawn.all_words()
    for w in sentence.words():
        options.add(w)
    while len(options) < difficulty:
        options.add(random.choice(words))

    return render(request, 'quiz/coze.html', {
        'sentence': sentence,
        'words': options,
        'corrects': corrects
    })

def coze_choice(request, uuid):
    pawn = get_object_or_404(Pawn, uuid=uuid)
    sentences = pawn.all_sentences()
    words = pawn.all_words()

    if request.method == 'POST':
        error = False
        for k,w in request.POST.items():
            try:
                id, word = k.split('_')
                sentence = get_object_or_404(Sentence, id=id)
                if not sentence.control({'word_' + word: w}):
                    error = True
            except Exception as e:
                print(e) 
        if error:
            messages.error(request, 'errato')
        else:
            messages.success(request, 'corretto')

    return render(request, 'quiz/coze-choice.html', {
        'sentences': sentences,
        'words': words
    }) 