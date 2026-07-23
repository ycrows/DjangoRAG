from django.urls import path
from . import views
from django.contrib import admin
from django.urls import include, path #from auth tutorial

from django.contrib.auth import views as auth_views


urlpatterns = [
    path('members/', views.members, name='members'),
    path('members/details/<int:id>', views.details, name='details'),
    path('myfirst/', views.myfirst, name='myfirst'),
    path('chat/', views.chat, name="chat"),
    path('', views.main, name="main"),
    path('testing/', views.testing, name='testing'),
    path('dashboard/', views.dashboard, name='dashboard'),    
    path('sign_up/', views.sign_up, name='sign_up'),
    path('preset', views.preset, name='preset'),
    path('save-preset/', views.save_preset, name="save_preset"),
    
    path('accounts/', include('django.contrib.auth.urls')),

]