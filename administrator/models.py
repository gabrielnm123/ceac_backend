from django.db import models

# Create your models here.

class Administrator(models.Model):
    class Meta:
        permissions = [
            # Operadores
            ('manageOperator', 'Gerenciar Operadores'),
            ('createOperator', 'Criar Operador'),

            # Perfil
            ('managePerfil', 'Gerenciar Perfis'),
            ('createPerfil', 'Criar Perfil'),
        ]
