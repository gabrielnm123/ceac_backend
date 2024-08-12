from rest_framework import serializers
from .models import Ficha, ModulosAprendizagem, FichaModulo

class FichaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ficha
        fields = '__all__'

class ModulosAprendizagemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModulosAprendizagem
        fields = '__all__'

class FichaModuloSerializer(serializers.ModelSerializer):
    class Meta:
        model = FichaModulo
        fields = '__all__'
