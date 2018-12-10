from django import forms
from .models import Estilo, Discografica
from django.conf import settings

class DiscograficaForm(forms.Form):
    nombre = forms.CharField(label='Nombre', max_length=100,
        widget=forms.TextInput(attrs={'placeholder' : 'Nombre'}))
    pais = forms.CharField(label='Pais', max_length=100,
        widget=forms.TextInput(attrs={'placeholder' : 'Pais'}))
    
class UsuarioForm(forms.Form):
    nombre = forms.CharField(label='Nombre', max_length=100)
    username = forms.CharField(label='Nombre de usuario', max_length=100)
    password = forms.CharField(label='Password', max_length=100)
    apellidos = forms.CharField(label='Apellidos', max_length=100)
    email = forms.EmailField(label='email', max_length=70)
    
class ArtistaForm(forms.Form):
    nombre = forms.CharField(label='Nombre', max_length=100,
        widget=forms.TextInput(attrs={'placeholder' : 'Nombre'}))
    pais = forms.CharField(label='Pais', max_length=100,
        widget=forms.TextInput(attrs={'placeholder' : 'Pais'}))
    fechNac = forms.DateField(label='Fecha de nacimiento', input_formats=settings.DATE_INPUT_FORMATS,
        widget=forms.TextInput(attrs={'placeholder' : 'YYYY-mm-dd'}))
    estilo = forms.ModelMultipleChoiceField(queryset=Estilo.objects.all())
    discografica = forms.ModelChoiceField(Discografica.objects.all())
    