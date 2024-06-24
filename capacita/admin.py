from django.contrib import admin
from .models import Ficha, Atividade
from django.http import HttpResponse
from docxtpl import DocxTemplate
import zipfile
import os
import tempfile
from django.db import models

class FichaAdmin(admin.ModelAdmin):
    search_fields = ['nome_completo', 'cpf']
    list_display = ('nome_completo', 'cpf')
    actions = ['download_ficha']
    production = 'capacita/doc/ficha.docx'
    is_production = os.path.isfile(production)
    dev = 'backend/capacita/doc/ficha.docx'
    is_dev = os.path.isfile(dev)
    context = dict()

    def __init__(self, model: type, admin_site: admin.AdminSite | None) -> None:
        if self.is_production:
            self.document = DocxTemplate(self.production)
        elif self.is_dev:
            self.document = DocxTemplate(self.dev)
        super().__init__(model, admin_site)

    def trata_ficha(self, ficha):
        for field in Ficha._meta.fields:
            campo = ficha._meta.get_field(field.name)
            # Verificar se o campo é uma instância de models.CharField e se tem choices
            ficha_element = getattr(ficha, field.name)
            if ficha_element:
                try:
                    ficha_element = ficha_element.strftime('%d/%m/%Y')
                    self.context[field.name] = str(ficha_element)
                except:
                    if isinstance(campo, models.CharField) and campo.choices:
                        # Obter o valor atual do campo
                        valor_campo = getattr(ficha, field.name)
                        # Encontrar a opção correspondente no atributo choices
                        opcoes = dict(campo.choices)
                        opcao_escolhida = opcoes.get(valor_campo)
                        # Imprimir a opção escolhida
                        self.context[field.name] = str(opcao_escolhida)
                    elif ficha_element == True:
                        self.context[field.name] = 'x'
                    else:
                        self.context[field.name] = str(ficha_element)
        self.document.render(self.context)

    def download_ficha(self, request, queryset):
        if len(queryset) > 1:
            zip_name = tempfile.mktemp(suffix=".zip")
            with zipfile.ZipFile(zip_name, 'w') as zip_file:
                for ficha in queryset:
                    self.trata_ficha(ficha)
                    doc_temp = tempfile.NamedTemporaryFile(delete=False)
                    self.document.save(doc_temp.name)
                    doc_temp.close()

                    zip_file.write(doc_temp.name, arcname=f'{ficha.nome_completo}.docx')
                    os.unlink(doc_temp.name)

            with open(zip_name, 'rb') as f:
                zip_data = f.read()

            response = HttpResponse(zip_data, content_type='application/zip')
            response['Content-Disposition'] = 'attachment; filename=fichas.zip'

            os.unlink(zip_name)
        else:
            for ficha in queryset:
                self.trata_ficha(ficha)
            response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
            response['Content-Disposition'] = f'attachment; filename="{ficha.nome_completo}.docx"'
            self.document.save(response)

        return response

    download_ficha.short_description = "Baixar ficha(s) selecionada(s)"

admin.site.register(Ficha, FichaAdmin)
admin.site.register(Atividade)
