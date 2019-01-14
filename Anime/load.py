import csv
import os, django
from pytz import timezone
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Anime.settings")
django.setup()

from main.models import *
import time
import datetime

with open('data/anime.csv', encoding='utf-8-sig') as csvfile:
    reader = csv.DictReader(csvfile, delimiter=';')
    for row in reader:
        anime_id = row['anime_id']
        title = row['name']
        genres = row['genre'].split(',')
        formato = row['type']
        numEpisodes = row['episodes']
        
        anime = Anime(animeId=anime_id, title=title, formato=formato, numEpisodes=numEpisodes)
        anime.save()
        genres_list = []
        for genre_name in genres:
        	if(Genre.objects.filter(name=genre_name).count()==0):
        		genre = Genre(name=genre_name)
        		genre.save()


        	anime.genre.add(Genre.objects.get(name=genre_name))

        

        print(anime)
