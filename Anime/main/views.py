import shelve
from .models import Anime, Genre, Rating
from main.forms import GenreForm, AnimeForm, UserForm
from django.shortcuts import render, get_object_or_404
from main.recommendations import  transformPrefs, calculateSimilarItems, getRecommendedItems, topMatches
from main.populate import populateDatabase

def loadDict():
    Prefs={}
    shelf = shelve.open("dataRS.dat")
    ratings = Rating.objects.all()
    for ra in ratings:
        userid = int(ra.userId)
        itemid = int(ra.animeId)
        rating = float(ra.rating)
        Prefs.setdefault(user, {})
        Prefs[userid][itemid] = rating
    shelf['Prefs']=Prefs
    shelf['ItemsPrefs']=transformPrefs(Prefs)
    shelf['SimItems']=calculateSimilarItems(Prefs, n=10)
    shelf.close()

def populateDB(request):
    populateDatabase() 
    return render(request,'populate.html')

def loadRS(request):
    loadDict()
    return render(request,'loadRS.html')

# APARTADO C
def similarAnimes(request):
    anime = None
    if request.method=='GET':
        form = AnimeForm(request.GET, request.FILES)
        if form.is_valid():
            idAnime = int(form.cleaned_data['id'])
            anime = get_object_or_404(Anime, pk=idAnime)
            shelf = shelve.open("dataRS.dat")
            ItemsPrefs = shelf['ItemsPrefs']
            shelf.close()
            recommended = topMatches(ItemsPrefs, idAnime,n=3)
            items=[]
            for re in recommended:
                item = Anime.objects.get(pk=int(re[1]))
                items.append(item)
            return render(request,'similarAnimes.html', {'anime': anime,'animes': items})
    form = AnimeForm()
    return render(request,'search_anime.html', {'form': form})

# APARTADO D
def recommendedAnimes(request):
    if request.method=='GET':
        form = UserForm(request.GET, request.FILES)
        if form.is_valid():
            userId = int(form.cleaned_data['id'])
            shelf = shelve.open("dataRS.dat")
            Prefs = shelf['Prefs']
            SimItems = shelf['SimItems']
            shelf.close()
            rankings = getRecommendedItems(Prefs, SimItems, userId)
            recommended = rankings[:2]
            items = []
            for re in recommended:
                item = Anime.objects.get(pk=re[1])
                items.append(item)
            return render(request,'recommendationItems.html', {'userId': userId, 'items': items})
