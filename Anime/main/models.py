from django.db import models
from django.core.validators import MinValueValidator,MaxValueValidator
# Create your models here.
class Genre(models.Model):
    name = models.CharField(max_length=20) 
    def __str__(self):
        return self.name

class Anime(models.Model):
    animeId = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=100)
    genre = models.ManyToManyField(Genre)
    formato = models.CharField(max_length=50)
    numEpisodes = models.IntegerField()

    def __str__(self):
        return self.title

class Rating(models.Model):
    userId = models.IntegerField()
    animeId = models.IntegerField()
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    def __str__(self):
        return str(self.rating)