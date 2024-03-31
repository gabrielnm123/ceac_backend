from django.contrib import admin
from .models import Ficha
from django.http import HttpResponse
from docxtpl import DocxTemplate

class FichaAdmin(admin.ModelAdmin):
    search_fields = ['nome_completo', 'cpf']
    list_display = ('nome_completo', 'cpf')
    actions = ['download_ficha']

    def download_ficha(self, request, queryset):
        document = DocxTemplate('backend/capacita/doc/FICHA.docx')
        context = dict()

        for ficha in queryset:
            for field in Ficha._meta.fields:
                value = getattr(ficha, field.name)
                if value:
                    context[field.name] = str(value)
        document.render(context)
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
        response['Content-Disposition'] = 'attachment; filename="ficha.docx"'
        document.save(response)
        return response

    download_ficha.short_description = "Baixar ficha(s) selecionada(s)"

admin.site.register(Ficha, FichaAdmin)
