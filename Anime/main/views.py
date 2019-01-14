from django.shortcuts import render, get_object_or_404
from .models import *
from .forms import *
# Create your views here.

#APARTADO A
def search(request):
    if request.method=='GET':
        form = GenreForm(request.GET, request.FILES)
        if form.is_valid():
            print("valido")
            requested = form.cleaned_data['genre']
            print(requested)
            allAnimes = Anime.objects.all()
            print(allAnimes)
            animes = []
            for anime in allAnimes:
                genres = []
                allGenres = anime.genre.all()
                print(allGenres)
                for genre in allGenres:
                    genres.append(genre.name)
                if requested in genres:
                    animes.append(anime)
                return render(request,'animes_genre.html', {'animes':animes})
    form=GenreForm()
    return render(request,'search_genre.html', {'form':form })