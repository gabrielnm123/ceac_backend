from rest_framework import serializers
from .models import Ficha, ModulosAprendizagem

class FichaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ficha
        fields = '__all__'

class ModulosAprendizagemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModulosAprendizagem
        fields = '__all__'
