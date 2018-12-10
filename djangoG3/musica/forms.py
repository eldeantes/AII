from django import forms
from .models import Estilo, Discografica

class DiscograficaForm(forms.Form):
    nombre = forms.CharField(label='Nombre', max_length=100)
    pais = forms.CharField(label='Pais', max_length=100)
    
class UsuarioForm(forms.Form):
    nombre = forms.CharField(label='Nombre', max_length=100)
    username = forms.CharField(label='Nombre de usuario', max_length=100)
    password = forms.CharField(label='Password', max_length=100)
    apellidos = forms.CharField(label='Apellidos', max_length=100)
    email = forms.EmailField(label='email', max_length=70)
    
class AstistaForm(forms.Form):
    nombre = forms.CharField(label='Nombre', max_length=100)
    pais = forms.CharField(label='Pais', max_length=100)
    fechNac = forms.DateField(label='Fecha de nacimiento')
    estilo = forms.ModelMultipleChoiceField(queryset=Estilo.objects.all())
    discografica = forms.ModelChoiceField(Discografica.objects.all())

class GetArtistasUsuario(forms.Form):
    name = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'placeholder' : 'Buscar'}))