from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('',views.index, name='index'),
    path('/new-discografica',views.newDiscografica, name='newDiscografica'),
    path('top-artistas/', views.topUsuarios, name='topUsuarios')
]
