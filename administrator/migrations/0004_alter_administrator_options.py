# Generated by Django 5.0.3 on 2025-01-03 18:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('administrator', '0003_alter_administrator_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='administrator',
            options={'permissions': [('searchUser', 'Buscar Usuário'), ('createUser', 'Criar Usuário'), ('editUser', 'Editar Usuário'), ('deleteUser', 'Deletar Usuário'), ('searchPerfil', 'Buscar Perfil'), ('createPerfil', 'Criar Perfil'), ('editPerfil', 'Editar Perfil'), ('deletePerfil', 'Deletar Perfil')]},
        ),
    ]
