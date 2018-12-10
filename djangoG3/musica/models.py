from django.db import models

# Create your models here.
class Discografica(models.Model):
    nombre = models.CharField(max_length=50)
    pais = models.CharField(max_length=30)

    def __str__(self):
        return self.nombre

class Usuario(models.Model):
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=50)
    nombre = models.CharField(max_length=20)
    apellidos = models.CharField(max_length=20)
    email = models.EmailField(max_length=70, null=True, blank=True, unique=True)

    def __str__(self):
        return self.nombre + ' ' + self.apellidos

class Artista(models.Model):
    nombre = models.CharField(max_length=30)
    pais = models.CharField(max_length=30)
    fechNac = models.DateField()

    discografica = models.ForeignKey(Discografica, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre