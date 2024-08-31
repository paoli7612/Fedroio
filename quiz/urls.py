from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='quiz'),
    path('new/<str:slug>', views.question_new, name='question.new'),
    path('<int:id>/edit', views.question_edit, name='question.edit'),
    path('<int:id>/delete', views.question_delete, name='question.delete'),
    path('<str:pawn_slug>', views.points, name='quiz.points')
]
