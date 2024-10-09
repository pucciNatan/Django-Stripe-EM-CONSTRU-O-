from django.db import models

class Produto(models.Model):
    nome = models.CharField(max_length=100)
    preco = models.FloatField()

    def __str__(self):
        return self.nome
    
    def exibirPreco(self):
        return "{:.2f}".format(self.preco)