from .models import Ficha, ModulosAprendizagem
from django_filters.rest_framework import (
    FilterSet,
    CharFilter,
    DateFilter,
    ModelChoiceFilter
)

class FichaFilter(FilterSet):
    nome = CharFilter(field_name='nome_completo', lookup_expr='icontains')
    modulo_aprendizagem = ModelChoiceFilter(queryset=ModulosAprendizagem.objects.all())
    cpf = CharFilter(field_name='cpf', lookup_expr='exact')
    data_nascimento = DateFilter(field_name='data_nascimento', lookup_expr='exact')
    genero = CharFilter(field_name='genero', lookup_expr='exact')
    escolaridade = CharFilter(field_name='escolaridade', lookup_expr='exact')
    uf = CharFilter(field_name='uf', lookup_expr='exact')
    atividade = CharFilter(field_name='atividade', lookup_expr='exact')
    celular = CharFilter(field_name='celular', lookup_expr='exact')
    fixo = CharFilter(field_name='fixo', lookup_expr='exact')
    email = CharFilter(field_name='email', lookup_expr='exact')

    class Meta:
        model = Ficha
        fields = [
            'nome',
            'modulo_aprendizagem',
            'cpf',
            'data_nascimento',
            'genero',
            'escolaridade',
            'uf',
            'atividade',
            'celular',
            'fixo',
            'email',
        ]
