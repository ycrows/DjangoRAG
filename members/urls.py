from django.urls import path
from . import views
from django.contrib import admin

urlpatterns = [
    path('members/', views.members, name='members'),
    path('members/details/<int:id>', views.details, name='details'),
    path('', views.home, name='home'),
    path('chat/', views.chat, name="chat"),

]