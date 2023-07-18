from django.db import models

# Create your models here.
class Usuario(models.Model):
    nome = models.CharField(max_length=120)
    email = models.EmailField(max_length=120)
    senha = models.CharField(max_length=64)


    def __str__(self) -> str:
        return self.nome