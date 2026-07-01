from django.urls import path
from . import views
from django.contrib import admin

urlpatterns = [
    path('members/', views.members, name='members'),
    path('members/details/<int:id>', views.details, name='details'),
    path('myfirst/', views.myfirst, name='myfirst'),
    path('chat/', views.chat, name="chat"),
    path('', views.main, name="main"),
    path('testing/', views.testing, name='testing'),

]