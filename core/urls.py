from django.urls import path, include, re_path

from . import views

urlpatterns = [
    path('account', views.account, name='account'),
    path('user/<int:id>', views.user, name='user'),
    path('user/<int:id>/delete', views.user_delete, name='user.delete'),
    path('user/<int:id>/reset', views.user_reset, name='user.reset'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/sign-up', views.signup, name='signup'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('edit-group/<int:id>', views.group_edit, name='core.group.edit'),
]
