from django.contrib import admin
from .models import Ficha
from django.http import HttpResponse
from docxtpl import DocxTemplate
import zipfile
import os
import tempfile

class FichaAdmin(admin.ModelAdmin):
    search_fields = ['nome_completo', 'cpf']
    list_display = ('nome_completo', 'cpf')
    actions = ['download_ficha']

    def download_ficha(self, request, queryset):
        # Cria um arquivo real para o arquivo zip
        zip_name = tempfile.mktemp(suffix=".zip")
        document = DocxTemplate('backend/capacita/doc/ficha.docx')
        if len(queryset) > 1:
            with zipfile.ZipFile(zip_name, 'w') as zip_file:
                for ficha in queryset:
                    context = dict()
                    for field in Ficha._meta.fields:
                        value = getattr(ficha, field.name)
                        if value:
                            context[field.name] = str(value)
                    document.render(context)
                    
                    # Salva o documento em um arquivo temporário
                    doc_temp = tempfile.NamedTemporaryFile(delete=False)
                    document.save(doc_temp.name)
                    doc_temp.close()

                    # Adiciona o arquivo temporário ao arquivo zip
                    zip_file.write(doc_temp.name, arcname=f'{ficha.nome_completo}.docx')
                    os.unlink(doc_temp.name)  # Remove o arquivo temporário

            # Lê o arquivo zip de volta para a resposta
            with open(zip_name, 'rb') as f:
                zip_data = f.read()

            # Configura a resposta para fazer o download do arquivo zip
            response = HttpResponse(zip_data, content_type='application/zip')
            response['Content-Disposition'] = 'attachment; filename=fichas.zip'
            
            # Remove o arquivo zip
            os.unlink(zip_name)
        else:
            context = dict()
            for ficha in queryset:
                for field in Ficha._meta.fields:
                    value = getattr(ficha, field.name)
                    if value:
                        context[field.name] = str(value)
            document.render(context)
            response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
            response['Content-Disposition'] = f'attachment; filename="{ficha.nome_completo}.docx"'
            document.save(response)

        return response

    download_ficha.short_description = "Baixar ficha(s) selecionada(s)"

admin.site.register(Ficha, FichaAdmin)
