from django.db import models

class Produto(models.Model):
    nome = models.CharField(max_length=100)
    preco = models.FloatField()

    def __str__(self):
        return self.nome
    
    def exibirPreco(self):
        return "{:.2f}".format(self.preco)
    
class Pedido(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    payment_intent = models.CharField(max_length=50, unique = True)
    email = models.EmailField()
    valor_pago = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50)

    def __str__(self):
        return f"Pedido de {self.email} - Produto: {self.produto.nome}"