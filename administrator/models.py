from django.db import models

# Create your models here.

class Administrator(models.Model):
    class Meta:
        permissions = [
            ('searchUser', 'Buscar Usuário'),
            ('createUser', 'Criar Usuário'),
            ('searchPerfil', 'Buscar Perfil'),
            ('createPerfil', 'Criar Perfil')
        ]
