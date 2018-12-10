from django.shortcuts import render, redirect
from . import models
from . import forms
from .models import Discografica, Artista, Tiempo

def index(request):
    return render(request, 'index.html')

def newDiscografica(request):
    if request.method == 'POST':
        form = forms.DiscograficaForm(request.POST)
        if form.is_valid():
            new_discografica = Discografica(nombre=request.POST['nombre'], pais=request.POST['pais'])
            new_discografica.save()
            return redirect('musica/')

    else:
        form = forms.DiscograficaForm()

    context = {'form' : form}
    return render(request, 'newDiscografica.html', context)

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