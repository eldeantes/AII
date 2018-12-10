from django.shortcuts import render

def index(request):
    return render(request, 'peliculas/index.html', context)

def newDiscografica(request):
    return render(request, 'peliculas/newDiscografica.html', context)

