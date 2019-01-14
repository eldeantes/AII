from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('',views.index, name='index'),
    path('ver-artistas/<slug:userId>/',views.verArtistas,name='verArtistas'),
    path('top-artistas/',views.topArtistas, name='topArtistas')
]
