from django.shortcuts import render
from django.db.models import Count
from .models import *


def index(request):
    return render(request, 'index.html')

def verArtistas(request, userId):
    usuarioArtista = UsuarioArtista.objects.filter(idUsuario=userId)
    artistas = []

    datos = []

    for entry in usuarioArtista:
        artista = Artista.objects.get(idArtista=entry.idArtista)
        artistas.append(artista)

    
    for artista, uA in zip(artistas, usuarioArtista):
        datos.append((artista,uA))

    context = {
            'userId': userId,
            'datos': datos,
    }
    return render(request, 'artistas.html',context)

def topArtistas(request):
    top = UsuarioArtista.objects.values_list('idArtista').annotate(artista_count=Count('idArtista')).order_by('-artista_count')
    top = top[:3]

    artista1 = Artista.objects.get(idArtista=top[0][0])
    artista2 = Artista.objects.get(idArtista=top[1][0])
    artista3 = Artista.objects.get(idArtista=top[2][0])

    context = {
        'artista1':artista1,
        'artista2':artista2,
        'artista3':artista3,
        'top':top
    }

    return render(request, 'top-artistas.html',context)