from .models import Ficha
from django_filters.rest_framework import (
    FilterSet,
    CharFilter,
    DateFilter,
)

class FichaFilter(FilterSet):
    nome = CharFilter(field_name='nome_completo', lookup_expr='icontains')
    cpf = CharFilter(field_name='cpf', lookup_expr='exact')
    data_nascimento = DateFilter(field_name='data_nascimento', lookup_expr='exact')
    genero = CharFilter(field_name='genero', lookup_expr='exact')
    escolaridade = CharFilter(field_name='escolaridade', lookup_expr='exact')
    uf = CharFilter(field_name='uf', lookup_expr='exact')
    atividade = CharFilter(field_name='atividade__atividade', lookup_expr='exact')
    contato = CharFilter(field_name='contato', lookup_expr='exact')
    email = CharFilter(field_name='email', lookup_expr='exact')

    class Meta:
        model = Ficha
        fields = [
            'nome',
            'cpf',
            'data_nascimento',
            'genero',
            'escolaridade',
            'uf',
            'atividade',
            'contato',
            'email'
        ]
