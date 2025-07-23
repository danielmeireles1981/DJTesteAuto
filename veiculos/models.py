from django.db import models

class Autobot(models.Model):
    nome = models.CharField(max_length=100)
    tipo = models.CharField(max_length=50)  # Ex: Carro, Caminhão, Moto
    poder = models.IntegerField()  # Força de combate
    frase_batalha = models.TextField()

    def __str__(self):
        return f"{self.nome} ({self.tipo})"