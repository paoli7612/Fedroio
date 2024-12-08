from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='interpares'),
    path('write/<int:id>', views.write, name='interpares.write'),
    path('evaluate', views.evaluate, name='interpares.evaluate'),
    path('evaluate7345678<int:id>6128676', views.evaluate, name='interpares.evaluate'),
    path('new-traccia', views.newTraccia, name='interpares.newTraccia'),
    path('delete-traccia/<int:id>', views.deleteTraccia, name='interpares.deleteTraccia'),
    path('print-traccia/<int:id>', views.printTraccia, name='interpares.printTraccia')
]


