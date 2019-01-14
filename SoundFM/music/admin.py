from django.contrib import admin
from .models import *

admin.site.register(Artista)
admin.site.register(UsuarioArtista)
admin.site.register(UsuarioEtiquetaArtista)
admin.site.register(Etiqueta)