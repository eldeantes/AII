from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('',views.index, name='index'),
    path('newDiscografica/',views.newDiscografica, name='newDiscografica'),
    path('newArtista/',views.newArtista, name='newArtista')
]
