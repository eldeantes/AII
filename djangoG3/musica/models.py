from django.db import models

# Create your models here.
class Discografica(models.Model):
    nombre = models.CharField(max_length=50)
    pais = models.CharField(max_length=30)

    def __str__(self):
        return self.nombre

class Estilo(models.Model):
    ROCK = 'Rock'
    POP = 'Pop'
    FUN = 'Fun'
    RAP = 'Rap'
    HEAVY = 'Heavy'
    TECHNO = 'Techno'
    PUNK = 'Punk'
    ESTILOS_CHOICES = (
        (ROCK, 'Rock'),
        (POP, 'Pop'),
        (FUN, 'Fun'),
        (RAP, 'Rap'),
        (HEAVY, 'Heavy'),
        (TECHNO, 'Techno'),
        (PUNK, 'Punk'),
    )
    name = models.CharField(max_length=20,choices=ESTILOS_CHOICES, unique=True)

    def __str__(self):
        return self.name

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

    estilo = models.ManyToManyField(Estilo)
    discografica = models.ForeignKey(Discografica, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre

class Tiempo(models.Model):
    tiempo = models.IntegerField()

    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    artista = models.ForeignKey(Artista, on_delete=models.CASCADE)

    def __str__(self):
        return self.usuario.name + '(' + self.tiempo + ')'
