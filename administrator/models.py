from django.db import models

# Create your models here.

class Administrator(models.Model):
    class Meta:
        permissions = [
            # Usuário
            ('searchUser', 'Buscar Usuário'),
            ('createUser', 'Criar Usuário'),
            ('editUser', 'Editar Usuário'),
            ('deleteUser', 'Deletar Usuário'),

            # Perfil
            ('searchPerfil', 'Buscar Perfil'),
            ('createPerfil', 'Criar Perfil'),
            ('editPerfil', 'Editar Perfil'),
            ('deletePerfil', 'Deletar Perfil'),
        ]
