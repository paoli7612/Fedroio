from django.urls import path, include, re_path

from . import views

urlpatterns = [
    path('account', views.account, name='account'),
    path('account/settings', views.settings, name='settings'),
    path('utente/<str:username>', views.user, name='user'),
    path('utente/<str:username>/delete', views.user_delete, name='user.delete'),
    path('utente/<str:username>/reset', views.user_reset, name='user.reset'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/sign-up', views.signup, name='signup'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('edit-group/<int:id>', views.group_edit, name='core.group.edit'),
    path('new-group', views.group_new, name='core.group.new'),
    path('edit-group/<int:id>/partis', views.group_partis, name='core.group.partis'),
    path('delete-group/<int:id>', views.group_delete, name='core.group.delete'),
]
