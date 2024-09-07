import random
from django.shortcuts import render, get_object_or_404, redirect
from django.db import IntegrityError
from django.urls import reverse
from django.contrib import messages
from .models import Pawn, Sentence, Question
from .forms import PawnForm, SentenceForm, QuestionForm

def index(request):
    return render(request, 'pawns/index.html', {
        'pawns': Pawn.objects.filter(parent=None),
    })

def pawn(request, slug):
    pawn = get_object_or_404(Pawn, slug=slug)
    return render(request, 'pawns/pawn.html', {
        'pawn': pawn
    })

def new_pawn(request, slug=None):
    parent_pawn = None
    if slug:
        parent_pawn = get_object_or_404(Pawn, slug=slug)
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
                return redirect(reverse('pawn', args=[pawn.slug]))
            except IntegrityError as e:
                form.fields['slug'].initial = form.cleaned_data['slug']
                if 'UNIQUE constraint failed' in str(e):
                    form.add_error('slug', f'{pawn.slug}: A pawn with this slug already exists.')
                else:
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

def edit_pawn(request, slug):
    pawn = get_object_or_404(Pawn, slug=slug)
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

def delete_pawn(request, slug):
    pawn = get_object_or_404(Pawn, slug=slug)
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

def edit_questions(request, slug):
    pawn = get_object_or_404(Pawn, slug=slug)
    if request.method == 'POST':
        messages.success(request, 'Questions updated successfully!')
        questions_text = request.POST.get('questions').strip()
        pawn.questions.all().delete()
        for r in questions_text.split('.'):
            if not '?' in r: continue
            try:
                r = r.strip()
                t, a = r.split('?')
                c, a1, a2, a3 = a.split(';')
                Question.objects.create(pawn = pawn, user = request.user, text = t, correct = c, a1 = a1, a2 = a2, a3 = a3)
            except:
                messages.error(request, "error at: " + r)
        return redirect(pawn.url())
    return render(request, 'pawns/edit-questions.html', {
        'pawn': pawn
    })

def new_sentence(request, slug):
    pawn = get_object_or_404(Pawn, slug=slug)
    if request.method == 'POST':
        form = SentenceForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'New sentence created!')
                return redirect(reverse('pawn', args=[pawn.slug]))
            except IntegrityError as e:
                form.fields['slug'].initial = form.cleaned_data['slug']
                if 'UNIQUE constraint failed' in str(e):
                    form.add_error('slug', f'{pawn.slug}: A pawn with this slug already exists.')
                else:
                    form.add_error(None, 'An error occurred while creating the pawn.')
    else:
        form = SentenceForm(initial={'pawn': pawn})

    return render(request, 'pawns/form.html', {
        'form': form,
        'pawn': pawn,
        'back_url': pawn.url()
    })

def new_question(request, slug):
    pawn = get_object_or_404(Pawn, slug=slug)
    if request.method == 'POST':
        form = QuestionForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'New sentence created!')
                return redirect(reverse('pawn', args=[pawn.slug]))
            except IntegrityError as e:
                form.fields['slug'].initial = form.cleaned_data['slug']
                if 'UNIQUE constraint failed' in str(e):
                    form.add_error('slug', f'{pawn.slug}: A pawn with this slug already exists.')
                else:
                    form.add_error(None, 'An error occurred while creating the pawn.')
    else:
        form = QuestionForm(initial={'pawn': pawn})

    return render(request, 'pawns/form.html', {
        'form': form,
        'pawn': pawn,
        'back_url': pawn.url()
    })

def quiz_points(request, slug):
    pawn = get_object_or_404(Pawn, slug=slug)
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
                return redirect(reverse('pawn.quiz-points', kwargs={'slug': slug}))
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

def coze_test(request, slug):
    pawn = get_object_or_404(Pawn, slug=slug)
    words = pawn.all_words()

    if request.method == 'POST':
        sentence = get_object_or_404(Sentence, id=int(request.POST.get('sentence_id')))
        kw = {key: value for key, value in request.POST.items() if key.startswith('word_')}
        if sentence.control(kw):
            messages.success(request, 'Corretto')
            sentence = random.choice(pawn.all_sentences())
        else:
            messages.error(request, 'Riprova')
    else:
        sentence = random.choice(pawn.all_sentences())

    return render(request, 'quiz/coze-test.html', {
        'sentence': sentence,
        'words': words
    })

def coze_choice(request, slug):
    pawn = get_object_or_404(Pawn, slug=slug)
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