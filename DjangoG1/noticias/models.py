from django.db import models
from .choices import *

# Create your models here.
class Diary(models.Model):
    name = models.CharField(max_length=20)
    country = models.CharField(max_length=20)
    language = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Author(models.Model):
    name = models.CharField(max_length=20)
    surname = models.CharField(max_length=20)
    email = models.EmailField(max_length=70, null=True, blank=True, unique=True)

    def __str__(self):
        return self.name + ' ' + self.surname


class News(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=40)
    summary = models.TextField(max_length=500)
    newsType = models.CharField(max_length=20, choices = TYPE_CHOICES, default = ACTUALIDAD)

    diary = models.ForeignKey(Diary, on_delete=models.CASCADE)
    author = models.ManyToManyField(Author)

    def __str__(self):
        return self.title


class User(models.Model):
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=50)
    name = models.CharField(max_length=20)
    surname = models.CharField(max_length=20)
    email = models.EmailField(max_length=70, null=True, blank=True, unique=True)

    news = models.ManyToManyField(News, blank=True)

    def __str__(self):
        return self.name + ' ' + self.surname