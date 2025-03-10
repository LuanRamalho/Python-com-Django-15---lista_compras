from django.db import models

class Nota(models.Model):
    titulo = models.CharField(max_length=255)
    anotacao_precos = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.titulo

class Item(models.Model):
    nota = models.ForeignKey(Nota, on_delete=models.CASCADE)
    nome_produto = models.CharField(max_length=255)
    quantidade_peso = models.FloatField()
    preco = models.FloatField()

    @property
    def sub_total(self):
        return round(self.quantidade_peso * self.preco, 2)
