# Generated by Django 5.0.3 on 2024-09-23 14:21

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('capacita', '0027_rename_modulosaprendizagem_moduloscapacita_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='ficha',
            name='data_criacao',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='DATA CRIAÇÃO:'),
        ),
    ]
