from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('',views.index, name='index'),
    path('new-discografica/',views.newDiscografica, name='newDiscografica'),
    path('artistas/', views.getArtistas, name='artistas'),
    path('artistas-populares/', views.getArtistasPopulares, name='artistas_populares'),
]
