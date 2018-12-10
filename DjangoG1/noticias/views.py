from django.shortcuts import render, redirect
from . import models
from . import forms
from .models import Diary

# Create your views here.
def diaries(request):
    diaries = Diary.objects.order_by('country')
    context = {'diaries' : diaries}
    return render(request, 'diaries.html', context)

def createDiary(request):

    if request.method == 'POST':
        form = forms.CreateDiary(request.POST)
        if form.is_valid():
            new_diary = Diary(name=request.POST['name'], country=request.POST['country'], language=request.POST['language'])
            new_diary.save()
            return redirect('diaries')

    else:
        form = forms.CreateDiary()

    context = {'form' : form}
    return render(request, 'createDiary.html', context)