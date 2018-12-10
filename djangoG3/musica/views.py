from django.shortcuts import render, redirect
from . import forms
from .models import *
import operator

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

def index(request):
    return render(request, 'index.html')

def newDiscografica(request):
    if request.method == 'POST':
        form = forms.DiscograficaForm(request.POST)
        if form.is_valid():
            new_discografica = Discografica(nombre=request.POST['nombre'], pais=request.POST['pais'])
            new_discografica.save()
            return redirect('')

    else:
        form = forms.DiscograficaForm()

    context = {'form' : form}
    return render(request, 'newDiscografica.html', context)

def newArtista(request):
    if request.method == 'POST':
        form = forms.ArtistaForm(request.POST)
        if form.is_valid():
            disc_id=request.POST['discografica']
            new_artista = Artista(nombre=request.POST['nombre'], pais=request.POST['pais'], fechNac=request.POST['fechNac'], discografica=Discografica.objects.get(id=disc_id))
            new_artista.save()
            new_artista.estilo.set(request.POST['estilo'])
            new_artista.save()
            return redirect('')

    else:
        form = forms.ArtistaForm()

    context = {'form' : form}
    return render(request, 'newArtista.html', context)

def getArtistasUsuario(request):
    form = forms.GetArtistasUsuario(request.GET)
    if form.is_valid():
        artistas = Artista.objects.filter(name__contains=request.GET['name'])
        context = {'artistas' : artistas}
        return render(request, 'artistas.html', context)

    else:
        form = forms.GetArtistasUsuario()

    context = {'form' : form}
    return render(request, 'getArtistasUsuario.html', context)
