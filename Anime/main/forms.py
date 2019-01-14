from django import forms

class GenreForm(forms.Form):
    genre = forms.CharField(label='genre')