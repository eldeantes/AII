# -*- encoding: utf-8 -*-
from django import forms
    
class AnimeForm(forms.Form):
    id = forms.CharField(label='Anime ID')

class UserForm(forms.Form):
    id = forms.CharField(label='User ID')

class GenreForm(forms.Form):
    genre = forms.CharField(label='genre')
