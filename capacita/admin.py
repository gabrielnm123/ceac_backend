from django.contrib import admin
from .models import Cliente, Atividade
from django.http import HttpResponse
from docxtpl import DocxTemplate
import zipfile
import os
import tempfile
from django.db import models

class ClienteAdmin(admin.ModelAdmin):
    search_fields = ['nome_completo', 'cpf']
    list_display = ('nome_completo', 'cpf')
    actions = ['download_cliente']
    production = 'capacita/doc/cliente.docx'
    is_production = os.path.isfile(production)
    dev = 'backend/capacita/doc/cliente.docx'
    is_dev = os.path.isfile(dev)
    context = dict()

    def __init__(self, model: type, admin_site: admin.AdminSite | None) -> None:
        if self.is_production:
            self.document = DocxTemplate(self.production)
        elif self.is_dev:
            self.document = DocxTemplate(self.dev)
        super().__init__(model, admin_site)

    def trata_cliente(self, cliente):
        for field in cliente._meta.fields:
            campo = cliente._meta.get_field(field.name)
            # Verificar se o campo é uma instância de models.CharField e se tem choices
            cliente_element = getattr(cliente, field.name)
            if cliente_element:
                try:
                    cliente_element = cliente_element.strftime('%d/%m/%Y')
                    self.context[field.name] = str(cliente_element)
                except:
                    if isinstance(campo, models.CharField) and campo.choices:
                        # Obter o valor atual do campo
                        valor_campo = getattr(cliente, field.name)
                        # Encontrar a opção correspondente no atributo choices
                        opcoes = dict(campo.choices)
                        opcao_escolhida = opcoes.get(valor_campo)
                        # Imprimir a opção escolhida
                        self.context[field.name] = str(opcao_escolhida)
                    elif cliente_element == True:
                        self.context[field.name] = 'x'
                    else:
                        self.context[field.name] = str(cliente_element)
        self.document.render(self.context)

    def download_cliente(self, request, queryset):
        if len(queryset) > 1:
            zip_name = tempfile.mktemp(suffix=".zip")
            with zipfile.ZipFile(zip_name, 'w') as zip_file:
                for cliente in queryset:
                    self.trata_cliente(cliente)
                    doc_temp = tempfile.NamedTemporaryFile(delete=False)
                    self.document.save(doc_temp.name)
                    doc_temp.close()

                    zip_file.write(doc_temp.name, arcname=f'{cliente.nome_completo}.docx')
                    os.unlink(doc_temp.name)

            with open(zip_name, 'rb') as f:
                zip_data = f.read()

            response = HttpResponse(zip_data, content_type='application/zip')
            response['Content-Disposition'] = 'attachment; filename=clientes.zip'

            os.unlink(zip_name)
        else:
            for cliente in queryset:
                self.trata_cliente(cliente)
            response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
            response['Content-Disposition'] = f'attachment; filename="{cliente.nome_completo}.docx"'
            self.document.save(response)

        return response

    download_cliente.short_description = "Baixar cliente(s) selecionado(s)"

admin.site.register(Cliente, ClienteAdmin)
admin.site.register(Atividade)
