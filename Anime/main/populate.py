from main.models import *
from datetime import datetime
import csv

path = "ml-100k"

def deleteTables():  
    Anime.objects.all().delete()
    Genre.objects.all().delete()
    Rating.objects.all().delete()
    
    
def populateAnime():
    print("Loading animes and genres...")
    
    with open('data/anime.csv', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        i=0
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
            
            i=i+1
            if(i==101): break
    print("Animes inserted: " + str(Anime.objects.count()))
    print("Genres inserted: " + str(Genre.objects.count()))
    
    print("---------------------------------------------------------")


def populateRatings():
    print("Loading ratings...")

    with open('data/ratings.csv', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        i=0
        for row in reader:
            anime_id = row['anime_id']
            user_id = row['user_id']
            rating = row['rating']
            
            ratingObject = Rating(animeId=anime_id, userId=user_id, rating=rating)
            ratingObject.save()
            i=i+1
            if(i==101): break
       
    print("Ratings inserted: " + str(Rating.objects.count()))
    print("---------------------------------------------------------")
    
    
def populateDatabase():
    deleteTables()
    populateRatings()
    populateAnime()
    print("Finished database population")
    
if __name__ == '__main__':
    populateDatabase()