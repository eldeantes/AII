from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Diary)
admin.site.register(News)
admin.site.register(User)
admin.site.register(Author)