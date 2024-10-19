from django.urls import path, include
from . import views

urlpatterns = [
    path('<str:uuid>', views.pawn, name='explore')

]


