# Generated by Django 5.0.3 on 2025-02-02 22:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('capacita', '0031_alter_ficha_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ficha',
            options={'permissions': [('searchFicha', 'Buscar Ficha'), ('createFicha', 'Criar Ficha')]},
        ),
    ]
