from django import forms

class CreateDiary(forms.Form):
    name = forms.CharField(max_length=20,
        widget=forms.TextInput(attrs={'placeholder' : 'Nombre'}))
    country = forms.CharField(max_length=20,
        widget=forms.TextInput(attrs={'placeholder' : 'País'}))
    language = forms.CharField(max_length=20,
        widget=forms.TextInput(attrs={'placeholder' : 'Idioma'}))