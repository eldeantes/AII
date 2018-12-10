from django import forms

class DiscograficaForm(forms.Form):
    nombre = forms.CharField(label='Nombre', max_length=100)
    pais = forms.CharField(label='Pais', max_length=100)
    
class UsuarioForm(forms.Form):
    nombre = forms.CharField(label='Nombre', max_length=100)
    username = forms.CharField(label='Nombre de usuario', max_length=100)
    password = forms.CharField(label='Password', max_length=100)
    apellidos = models.CharField(label='Apellidos', max_length=100)
    email = models.EmailField(label='email', max_length=70, null=True, blank=True, unique=True)
    
class AstistaForm(forms.Form):
    nombre = forms.CharField(label='Nombre', max_length=100)
    pais = forms.CharField(label='Pais', max_length=100)

class GetArtistasUsuario(forms.Form):
    name = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'placeholder' : 'Buscar'}))
    