from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='pawns'),
    path('new', views.new_pawn, name='pawn.new'),
    path('<str:slug>', views.pawn, name='pawn'),
    path('<str:slug>/new', views.new_pawn, name='pawn.new'),
    path('<str:slug>/edit', views.edit_pawn, name='pawn.edit'),
    path('<str:slug>/delete', views.delete_pawn, name='pawn.delete'),

    path('<str:slug>/new-sentence', views.new_sentence, name='pawn.sentence-new'),
    path('<str:slug>/new-question', views.new_question, name='pawn.question-new'),
    
    path('sentence/<int:id>/edit', views.edit_sentence, name='pawns.sentence-edit'),
    path('question/<int:id>/edit', views.edit_question, name='pawns.question-edit'),

    path('sentence/<int:id>/delete', views.delete_sentence, name='pawns.sentence-delete'),
    path('question/<int:id>/delete', views.delete_question, name='pawns.question-delete'),
    path('<str:slug>/quiz/punti', views.quiz_points, name='pawn.quiz-points'),
    #path('<str:pawn_slug>/catena', views.chain, name='quiz.chain'),
    path('<str:slug>/coze-test', views.coze_test, name='pawn.quiz-coze'),
    path('<str:slug>/coze-choice', views.coze_choice, name='pawn.choice-coze')
   
]


