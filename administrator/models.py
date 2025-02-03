from django.db import models

# Create your models here.

class Administrator(models.Model):
    class Meta:
        permissions = [
            # Usuário
            ('manageUser', 'Gerenciar Usuário'),
            ('createUser', 'Criar Usuário'),

            # Perfil
            ('managePerfil', 'Gerenciar Perfil'),
            ('createPerfil', 'Criar Perfil'),
        ]
