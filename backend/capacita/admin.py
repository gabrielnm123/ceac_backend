from django.contrib import admin
from .models import Ficha

class FichaAdmin(admin.ModelAdmin):
    search_fields = ['nome_completo', 'cpf']
    list_display = ('nome_completo', 'cpf')

admin.site.register(Ficha, FichaAdmin)
