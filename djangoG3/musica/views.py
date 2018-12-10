from django.shortcuts import render
from .models import Artista, Tiempo
from . import forms

def index(request):
    return render(request, 'peliculas/index.html', context)

def newDiscografica(request):
    return render(request, 'peliculas/newDiscografica.html', context)

# def topArtistas(request):
#     tiempos = Tiempo.objects.filter(artista_exact(''))
#     artistas = Artista.objects.values('id').annotate(tiempo_count=Count('jobtitle')).order_by('tiempo')[:2]
#     context = {'artistas' : artistas}
#     return render(request, 'artistas.html', context)

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