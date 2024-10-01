from django.contrib import admin
from .models import Ficha, ModulosCapacita
from django.http import HttpResponse
from docxtpl import DocxTemplate
import zipfile
import os
import tempfile
from django.db import models

class FichaAdmin(admin.ModelAdmin):
    search_fields = ['nome_completo', 'cpf']
    list_display = ['id', 'nome_completo', 'cpf']
    actions = ['download_ficha']
    template_path = 'capacita/doc/ficha.docx'
    context = dict()

    def __init__(self, model: type, admin_site: admin.AdminSite | None) -> None:
        if os.path.isfile(self.template_path):
            self.document = DocxTemplate(self.template_path)
        super().__init__(model, admin_site)

    def trata_ficha(self, ficha):
        for field in ficha._meta.fields:
            campo = ficha._meta.get_field(field.name)
            ficha_element = getattr(ficha, field.name)
            if ficha_element:
                if isinstance(campo, models.DateField):
                    ficha_element = ficha_element.strftime('%d/%m/%Y')
                    self.context[field.name] = str(ficha_element)
                elif isinstance(campo, models.CharField) and campo.choices:
                    valor_campo = getattr(ficha, field.name)
                    opcoes = dict(campo.choices)
                    opcao_escolhida = opcoes.get(valor_campo)
                    self.context[field.name] = str(opcao_escolhida)
                elif field.name == 'cpf':
                    # Formatação padrão para CPF: 123.456.789-10
                    self.context[field.name] = f"{ficha_element[:3]}.{ficha_element[3:6]}.{ficha_element[6:9]}-{ficha_element[9:]}"
                elif field.name == 'cnpj':
                    # Formatação padrão para CNPJ: 12.345.678/0001-90
                    self.context[field.name] = f"{ficha_element[:2]}.{ficha_element[2:5]}.{ficha_element[5:8]}/{ficha_element[8:12]}-{ficha_element[12:]}"
                elif field.name == 'fixo':
                    # Formatação padrão para telefone fixo: (12) 3456-7890
                    self.context[field.name] = f"({ficha_element[:2]}) {ficha_element[2:6]}-{ficha_element[6:]}"
                elif field.name == 'celular':
                    # Formatação padrão para celular: (12) 9 8765-4321
                    self.context[field.name] = f"({ficha_element[:2]}) {ficha_element[2]} {ficha_element[3:7]}-{ficha_element[7:]}"
                elif field.name == 'cep':
                    # Formatação padrão para CEP: 12345-678
                    self.context[field.name] = f"{ficha_element[:5]}-{ficha_element[5:]}"
                else:
                    self.context[field.name] = str(ficha_element) if ficha_element else ''  # Se o campo estiver None, fica vazio
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

    download_ficha.short_description = "Baixar ficha(s) selecionado(s)"

class ModulosCapacitaAdmin(admin.ModelAdmin):
    search_fields = ['nome']
    list_display = ['id', 'nome', 'descricao']

admin.site.register(Ficha, FichaAdmin)
admin.site.register(ModulosCapacita, ModulosCapacitaAdmin)
