from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='pawns'),
    path('new-pawn', views.new_pawn, name='pawn.new'),
    path('<str:slug>', views.pawn, name='pawn'),
    path('<str:slug>/new-pawn', views.new_pawn, name='pawn.new'),
    path('<str:slug>/edit-pawn', views.edit_pawn, name='pawn.edit'),
    path('<str:slug>/edit-questions-pawn', views.edit_questions, name='pawn.edit-questions'),
    path('<str:slug>/delete-pawn', views.delete_pawn, name='pawn.delete')
]
