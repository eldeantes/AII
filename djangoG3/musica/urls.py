from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('',views.index, name='index'),
    path('artistas/', views.getArtistas, name='artistas'),
    path('artistas-populares/', views.getArtistasPopulares, name='artistas_populares'),
    path('newDiscografica/',views.newDiscografica, name='newDiscografica'),
    path('newArtista/',views.newArtista, name='newArtista'),
    path('newUsuario/',views.newUsuario, name='newUsuario')
]
