from django.db import models

# Create your models here.

class Administrator(models.Model):
    class Meta:
        permissions = [
            ("operadores", "Operadores"),
            ("perfis", "Perfis de Acesso"),
        ]
