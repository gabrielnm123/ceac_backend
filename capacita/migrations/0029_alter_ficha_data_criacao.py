# Generated by Django 5.0.3 on 2024-10-21 12:08

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('capacita', '0028_ficha_data_criacao'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ficha',
            name='data_criacao',
            field=models.DateField(default=datetime.date.today, verbose_name='DATA CRIAÇÃO:'),
        ),
    ]
