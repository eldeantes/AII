from django.shortcuts import render
from .models import *
import operator

def index(request):
    return render(request, 'musica/index.html', context)

def newDiscografica(request):
    return render(request, 'musica/newDiscografica.html', context)

def getArtistas(request):
    artistas = Artista.objects.order_by('discografica')
    context = {'artistas' : artistas}
    return render(request, 'artistas.html', context)

def getArtistasPopulares(request):
    tiempos = Tiempo.objects.all()
    artistas = {}
    for t in tiempos:
        artista = t.artista
        if artista in artistas:
            artistas[artista] = artistas.get(artista) + t.tiempo
        else:
            artistas[artista] = t.tiempo

    artistasPopulares=[]
    artistaPopular = max(artistas.items(), key=operator.itemgetter(1))[0]
    artistasPopulares.append(artistaPopular)
    del artistas[artistaPopular]
    artistaPopular = max(artistas.items(), key=operator.itemgetter(1))[0]
    artistasPopulares.append(artistaPopular)
    
    context = {'artistas' : artistasPopulares}
    return render(request, 'artistas_populares.html', context)

