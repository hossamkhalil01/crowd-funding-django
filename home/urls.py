from django.urls import include, path
from django.contrib import admin
from . import views

urlpatterns = [
    path('home/', views.index, name='home'),
]