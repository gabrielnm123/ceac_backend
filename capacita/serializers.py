from rest_framework import serializers
from .models import Ficha, ModulosCapacita

class FichaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ficha
        fields = '__all__'

class ModulosCapacitaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModulosCapacita
        fields = '__all__'
