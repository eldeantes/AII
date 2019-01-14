from django.db import models
from datetime import datetime

class Artista(models.Model):
    idArtista = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=100)
    url = models.CharField(max_length=100)
    pictureUrl = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Etiqueta(models.Model):
    idTag = models.IntegerField(primary_key=True)
    tagValue = models.CharField(max_length=100)

    def __str__(self):
        return self.tagValue

class UsuarioArtista(models.Model):
    idArtista = models.IntegerField()
    idUsuario = models.IntegerField()
    tiempoEscucha = models.IntegerField()

class UsuarioEtiquetaArtista(models.Model):
    idArtista = models.IntegerField()
    idUsuario = models.IntegerField()
    idTag = models.IntegerField()
    fecha = models.DateTimeField()    