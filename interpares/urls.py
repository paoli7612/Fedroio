from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='interpares'),
    path('write', views.write, name='interpares.write'),
    path('evaluate', views.evaluate, name='interpares.evaluate')
]


