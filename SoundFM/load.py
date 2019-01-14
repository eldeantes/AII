import os, django
from pytz import timezone
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SoundFM.settings")
django.setup()

from music.models import *
import time
import datetime



#Datos de artista
def cargarArtistas():
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


#Datos de etiqueta
def cargarEtiquetas():
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

def cargarUsuarioArtista():
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

def cargarUsuarioEtiquetaArtista():
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


option = ''
while(option!='q'):
	print("Introduce una opción (para salir, introduce q):\n")
	print("1 - Cargar datos de Artistas")
	print("2 - Cargar datos de Etiquetas")
	print("3 - Cargar datos de UsuarioArtista")
	print("4 - Cargar datos de UsuarioEtiquetaArtista")

	option = input()

	if(option=='1'):
		cargarArtistas()
	elif(option=='2'):
		cargarEtiquetas()
	elif(option=='3'):
		cargarUsuarioArtista()
	elif(option=='4'):
		cargarUsuarioEtiquetaArtista()