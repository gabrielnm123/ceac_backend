from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .filters import FichaFilter
from .models import Ficha, ModulosCapacita
from .serializers import FichaSerializer, ModulosCapacitaSerializer
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
    authentication_classes = [authentication.JWTAuthentication]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = FichaFilter
    ordering_fields = '__all__'

class ModulosCapacitaViewSet(viewsets.ModelViewSet):
    queryset = ModulosCapacita.objects.all()
    serializer_class = ModulosCapacitaSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.JWTAuthentication]

def download_ficha_view(request, ficha_id):
    template_path = 'capacita/doc/ficha.docx'

    if not os.path.isfile(template_path):
        return HttpResponse("Template de ficha não encontrado.", status=404)

    document = DocxTemplate(template_path)
    ficha = get_object_or_404(Ficha, id=ficha_id)
    context = {}

    for field in ficha._meta.fields:
        campo = ficha._meta.get_field(field.name)
        ficha_element = getattr(ficha, field.name)
        if ficha_element:
            if isinstance(campo, models.DateField):
                ficha_element = ficha_element.strftime('%d/%m/%Y')
                context[field.name] = str(ficha_element)
            elif isinstance(campo, models.CharField) and campo.choices:
                valor_campo = getattr(ficha, field.name)
                opcoes = dict(campo.choices)
                opcao_escolhida = opcoes.get(valor_campo)
                context[field.name] = str(opcao_escolhida)
            elif field.name == 'cpf':
                # Formatação padrão para CPF: 123.456.789-10
                context[field.name] = f"{ficha_element[:3]}.{ficha_element[3:6]}.{ficha_element[6:9]}-{ficha_element[9:]}"
            elif field.name == 'cnpj':
                # Formatação padrão para CNPJ: 12.345.678/0001-90
                context[field.name] = f"{ficha_element[:2]}.{ficha_element[2:5]}.{ficha_element[5:8]}/{ficha_element[8:12]}-{ficha_element[12:]}"
            elif field.name == 'fixo':
                # Formatação padrão para telefone fixo: (12) 3456-7890
                context[field.name] = f"({ficha_element[:2]}) {ficha_element[2:6]}-{ficha_element[6:]}"
            elif field.name == 'celular':
                # Formatação padrão para celular: (12) 9 8765-4321
                context[field.name] = f"({ficha_element[:2]}) {ficha_element[2]} {ficha_element[3:7]}-{ficha_element[7:]}"
            elif field.name == 'cep':
                # Formatação padrão para CEP: 12345-678
                context[field.name] = f"{ficha_element[:5]}-{ficha_element[5:]}"
            else:
                context[field.name] = str(ficha_element) if ficha_element else ''  # Se o campo estiver None, fica vazio

    document.render(context)
    
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.docx')
    document.save(temp_file.name)
    temp_file.close()

    with open(temp_file.name, 'rb') as f:
        file_data = f.read()
        response = HttpResponse(file_data, content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
        filename = re.sub(r'[^\w\s-]', '', ficha.nome_completo).strip().rstrip('-.')
        response['Content-Disposition'] = f'attachment; filename="{filename}.docx"'
    os.unlink(temp_file.name)

    return response
