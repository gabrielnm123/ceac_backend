# Generated by Django 5.0.3 on 2025-02-02 22:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('administrator', '0005_alter_administrator_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='administrator',
            options={'permissions': [('manageUser', 'Buscar Usuário'), ('createUser', 'Criar Usuário'), ('managePerfil', 'Buscar Perfil'), ('createPerfil', 'Criar Perfil')]},
        ),
    ]
