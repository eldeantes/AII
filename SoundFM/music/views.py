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

def populate(request):
    #Datos de artista
    file = open('music/data/artists.dat','r', encoding="utf8") 

    i = 0

    for line in file:
        print(line)
        #La primera linea no aporta información
        if(i!=0):
            datos = line.split('\t')
            artista = Artista(idArtista=datos[0], nombre=datos[1], url=datos[2], pictureUrl=datos[3])
            artista.save()

        i = i+1
    file.close()

    file = open('music/data/tags.dat', 'r', encoding='latin-1')
    i = 0
    for line in file:
        print(line)
        if(i!=0):
            datos = line.split('\t')
            tag = Etiqueta(idTag = datos[0], tagValue=datos[1])
            tag.save()
        i = i+1

    file.close()

    file = open('music/data/user_artists.dat', 'r', encoding='utf8')
    i = 0
    for line in file:
        print(line)
        if(i!=0):
            datos = line.split('\t')
            usuarioArtista = UsuarioArtista(idUsuario = datos[0], idArtista=datos[1], tiempoEscucha=datos[2])
            usuarioArtista.save()
        i = i+1

    file.close()

    file = open('music/data/user_taggedartists.dat', 'r', encoding='utf8')
    i = 0
    for line in file:
        print(line)
        if(i!=0):
            datos = line.split('\t')
            datos[3] = datos[3].strip()
            datos[4] = datos[4].strip()
            datos[5] = datos[5].strip()
            
            date = datos[3]+'/'+datos[4]+'/'+datos[5]

            date = datetime.datetime.strptime(date, "%d/%m/%Y")
            fmdate = date.replace(tzinfo=timezone('UTC'))
            usuarioEtiquetaArtista = UsuarioEtiquetaArtista(idUsuario = datos[0], idArtista=datos[1], idTag=datos[2], fecha = fmdate)
            usuarioEtiquetaArtista.save()
        i = i+1

    file.close()
    return render(request, 'index.html')

