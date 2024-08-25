from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib import messages
from random import choice

from .models import Question, Answer
from .forms import QuestionForm

from pawns.models import Pawn


# Create your views here.
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
        'form': form
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
    questions = pawn.all_questions()
    if request.method == 'GET':
        request.session['points'] = 0
        request.session['answered_questions'] = []
        question = choice(questions)
    else:
        question_id = request.POST.get('id')
        question = get_object_or_404(Question, id=question_id)

        if request.POST.get('answer') == '0':
            if question_id in request.session['answered_questions']:
                messages.error(request, 'Hai già risposto a questa domanda!')
                return redirect(reverse('quiz.points', kwargs={'pawn_slug': pawn_slug}))
            request.session['points'] += 1
            messages.success(request, 'Corretto')
            answer, _ = Answer.objects.get_or_create(question=question, user=request.user)
            answer.correctly += 1
            answer.save()
            request.session['answered_questions'].append(question_id)
            questions_filtered = [question for question in questions if str(question.id) not in request.session['answered_questions']]
            if len(questions_filtered) == 0:
                messages.success(request, 'Risposte completate :D')
                return redirect(reverse('profile'))
            question = choice(questions_filtered)
            while question.id in request.session['answered_questions']:
                questions_filtered.remove(question)
                question = choice(questions_filtered)
        else:
            Answer.objects.create(question=question, user=request.user, state=False)
            messages.error(request, 'Errore')
            return redirect(reverse('quiz.points', kwargs={'pawn_slug': pawn_slug}))

    return render(request, 'quiz/points.html', {
        'points': request.session['points'],
        'question': question
    })