from django.urls import path, include, re_path

from . import views

urlpatterns = [
    path('account', views.account, name='account'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/sign-up', views.signup, name='signup'),
]
