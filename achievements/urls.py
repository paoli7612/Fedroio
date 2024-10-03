from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='achievements'),
    path('leaderboard', views.leaderboard, name='achievements.leaderboard'),
]


