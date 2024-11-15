from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='pawns'),
    path('new', views.new_pawn, name='pawn.new'),
    path('<uuid:uuid>', views.pawn, name='pawn'),
    path('<uuid:uuid>/new', views.new_pawn, name='pawn.new'),
    path('<uuid:uuid>/edit', views.edit_pawn, name='pawn.edit'),
    path('<uuid:uuid>/delete', views.delete_pawn, name='pawn.delete'),

    path('<uuid:uuid>/new-sentence', views.new_sentence, name='pawn.sentence-new'),
    path('<uuid:uuid>/new-question', views.new_question, name='pawn.question-new'),
    path('<uuid:uuid>/new-questions', views.new_questions, name='pawn.questions-new'),
    
    path('sentence/<int:id>/edit', views.edit_sentence, name='pawns.sentence-edit'),
    path('question/<int:id>/edit', views.edit_question, name='pawns.question-edit'),
    path('sentence/<int:id>/delete', views.delete_sentence, name='pawns.sentence-delete'),
    path('question/<int:id>/delete', views.delete_question, name='pawns.question-delete'),

    path('<uuid:uuid>/esame', views.exam, name='pawn.exam'),
    path('<uuid:uuid>/quiz/punti-difficile', views.quiz_pointsHard, name='pawn.quiz-pointsHard'),
    path('<uuid:uuid>/quiz/punti', views.quiz_points, name='pawn.quiz-points'),
    path('<uuid:uuid>/quiz/catena', views.quiz_chain, name='pawn.quiz-chain'),
    path('<uuid:uuid>/coze/<int:difficulty>', views.coze_points, name='pawn.coze'),

    path('<uuid:uuid>/partis', views.partis, name='pawn.partis')

   
]


