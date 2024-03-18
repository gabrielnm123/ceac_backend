from rest_framework import serializers
from .models import Ficha

class FichaSerializer(serializers.ModelSerializer):
    # data_abertura = serializers.DateField(format="%d/%m/%Y", read_only=True)
    # data_nascimento = serializers.DateField(format="%d/%m/%Y", read_only=True)
    # data_criacao = serializers.DateTimeField(format="%d/%m/%Y %H:%M:%S", read_only=True)

    class Meta:
        model = Ficha
        fields = '__all__'
