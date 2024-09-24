from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .filters import FichaFilter
from .models import Ficha, ModulosCapacita
from .serializers import FichaSerializer, ModulosCapacitaSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt import authentication
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from docxtpl import DocxTemplate
import tempfile
import os
from django.db import models
import re  # Para usar expressões regulares para formatação

class FichaViewSet(viewsets.ModelViewSet):
    queryset = Ficha.objects.all()
    serializer_class = FichaSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = FichaFilter
    ordering_fields = '__all__'

class ModulosCapacitaViewSet(viewsets.ModelViewSet):
    queryset = ModulosCapacita.objects.all()
    serializer_class = ModulosCapacitaSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.JWTAuthentication]

def format_field(value, pattern):
    """Formata o campo de acordo com o padrão especificado."""
    if value and isinstance(value, str):
        return re.sub(pattern[0], pattern[1], value)
    return value

def download_ficha_view(request, ficha_id):
    # Define o caminho dos templates
    production = 'capacita/doc/ficha.docx'
    dev = 'backend/capacita/doc/ficha.docx'

    # Verifica se o arquivo existe no caminho de produção ou de desenvolvimento
    is_production = os.path.isfile(production)
    is_dev = os.path.isfile(dev)

    # Carrega o documento de acordo com o ambiente
    if is_production:
        document = DocxTemplate(production)
    elif is_dev:
        document = DocxTemplate(dev)
    else:
        return HttpResponse("Template de ficha não encontrado.", status=404)

    # Obtenha a ficha pelo ID
    ficha = get_object_or_404(Ficha, id=ficha_id)
    context = {}

    # Função para tratar a ficha e preencher o contexto com formatações
    for field in ficha._meta.fields:
        campo = ficha._meta.get_field(field.name)
        ficha_element = getattr(ficha, field.name)
        if ficha_element:
            try:
                ficha_element = ficha_element.strftime('%d/%m/%Y')
                context[field.name] = str(ficha_element)
            except:
                if isinstance(campo, models.CharField) and campo.choices:
                    valor_campo = getattr(ficha, field.name)
                    opcoes = dict(campo.choices)
                    opcao_escolhida = opcoes.get(valor_campo)
                    context[field.name] = str(opcao_escolhida)
                elif ficha_element == True:
                    context[field.name] = 'x'
                else:
                    # Adicione formatação para campos específicos aqui
                    if field.name == 'cpf':
                        context[field.name] = format_field(ficha_element, (r'(\d{3})(\d{3})(\d{3})(\d{2})', r'\1.\2.\3-\4'))
                    elif field.name == 'cnpj':
                        context[field.name] = format_field(ficha_element, (r'(\d{2})(\d{3})(\d{3})(\d{4})(\d{2})', r'\1.\2.\3/\4-\5'))
                    elif field.name == 'fixo':
                        context[field.name] = format_field(ficha_element, (r'(\d{2})(\d{4})(\d{4})', r'(\1) \2-\3'))
                    elif field.name == 'celular':
                        context[field.name] = format_field(ficha_element, (r'(\d{2})(\d{1})(\d{4})(\d{4})', r'(\1) \2 \3-\4'))
                    elif field.name == 'cep':
                        context[field.name] = format_field(ficha_element, (r'(\d{5})(\d{3})', r'\1-\2'))
                    else:
                        context[field.name] = str(ficha_element)

    # Renderiza o documento com o contexto
    document.render(context)

    # Cria um arquivo temporário para salvar o documento modificado
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.docx')
    document.save(temp_file.name)
    temp_file.close()

    # Lê o arquivo e retorna como resposta para download
    with open(temp_file.name, 'rb') as f:
        file_data = f.read()
        response = HttpResponse(file_data, content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
        response['Content-Disposition'] = f'attachment; filename="{ficha.nome_completo}.docx"'

    # Remove o arquivo temporário
    os.unlink(temp_file.name)

    return response
