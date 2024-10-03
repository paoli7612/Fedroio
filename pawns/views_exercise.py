import random
from django.db.models import Case, When 
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib import messages
from .models import Pawn, Sentence, Question

def quiz_points(request, uuid):
    pawn = get_object_or_404(Pawn, uuid=uuid)
    questions = pawn.all_questions()

    if request.method == 'GET': 
        request.session['quiz-points'] = 0
        request.session['quiz-answered'] = [] 
        question = random.choice(questions)

    elif request.method == 'POST':
        question_id = request.POST.get('id')
        question = get_object_or_404(Question, id=question_id)

        if request.POST.get('answer') == '0':
            if question_id in request.session['quiz-answered']:
                messages.error(request, 'Hai già risposto a questa domanda!')
                return redirect(reverse('pawn.quiz-points', kwargs={'uuid': uuid}))
            else: 
                question.answer(True)
                request.session['quiz-points'] += 1 
                messages.success(request, 'Corretto')
                request.session['quiz-answered'].append(question_id)
                questions_filtered = [question for question in questions if str(question.id) not in request.session['quiz-answered']] # prendo le domande che non ho ancora risposto
                if len(questions_filtered) == 0: 
                    messages.success(request, 'Risposte completate :D')
                    return redirect(reverse('account'))
                else: 
                    question = random.choice(questions_filtered)
        else: 
            question.answer(False)
            messages.error(request, 'Errore')
            request.session['quiz-points'] = 0
            request.session['quiz-answered'] = [] 

    return render(request, 'quiz/points.html', {
        'points': request.session['quiz-points'],
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
        question_id = request.POST.get('id')
        question = get_object_or_404(Question, id=question_id)
        chain_ids = request.session['chain']
        order = Case(*[When(id=pk, then=pos) for pos, pk in enumerate(chain_ids)])
        chain = list(Question.objects.filter(id__in=chain_ids).order_by(order))
        if request.POST.get('answer') == '0':
            question.wrong_answerw
            messages.success(request, 'Corretto') # messaggio "corretto"
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
            request.session['points'] = 0
            nextQuestion = chain[0]
        
    return render(request, 'quiz/chain.html', {
        'points': request.session['points']+1,
        'question': nextQuestion,
        'questions': chain
    })

def coze_points(request, uuid, difficulty):
    pawn = get_object_or_404(Pawn, uuid=uuid)

    if request.method == 'POST':
        sentence_id = request.POST.get('sentence_id')
        sentence = get_object_or_404(Sentence, id=sentence_id)

        input_words = request.POST.getlist('words[]')
        corrects = sentence.control(input_words)
        if len(corrects) == len(input_words):
            messages.success(request, 'Corretto')
            request.session['coze-answered'].append(sentence.id)
            if len(pawn.all_sentences()) == len(request.session['coze-answered']):
                messages.success(request, 'Risposte completate :D')
                return redirect(reverse('account'))
            sentence = random.choice(pawn.all_sentences())
            while sentence.id in request.session['coze-answered']:
                sentence = random.choice(pawn.all_sentences())
            request.session['coze-points'] += len(corrects)
            corrects = list()
        else:
            messages.error(request, 'Riprova')
            request.session['coze-points'] = 0
            request.session['coze-answered'] = [] 
    elif request.method == 'GET':
        sentence = random.choice(pawn.all_sentences())
        corrects = list()
        
        request.session['coze-points'] = 0
        request.session['coze-answered'] = list()

    options = set()
    words = pawn.all_words()
    for w in sentence.words():
        options.add(w)
    while len(options) < difficulty*4:
        options.add(random.choice(words))

    return render(request, 'quiz/coze.html', {
        'sentence': sentence,
        'options': options,
        'corrects': corrects,
        'points': request.session['coze-points'],
        'difficulty': difficulty
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
