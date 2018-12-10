from django.shortcuts import render, redirect
from . import models
from . import forms
from .models import Discografica, Artista, Tiempo, Usuario

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

def newUsuario(request):
    if request.method == 'POST':
        form = forms.UsuarioForm(request.POST)
        if form.is_valid():
            new_usuario = Usuario(username=request.POST['username'],password=request.POST['password'],nombre=request.POST['nombre'], apellidos=request.POST['apellidos'], email=request.POST['email'])
            new_usuario.save()
            return redirect('')

    else:
        form = forms.UsuarioForm()

    context = {'form' : form}
    return render(request, 'newUsuario.html', context)

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
