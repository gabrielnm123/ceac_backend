# Generated by Django 5.0.3 on 2025-02-02 22:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('administrator', '0006_alter_administrator_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='administrator',
            options={'permissions': [('manageUser', 'Gerenciar Usuário'), ('createUser', 'Criar Usuário'), ('managePerfil', 'Gerenciar Perfil'), ('createPerfil', 'Criar Perfil')]},
        ),
    ]
