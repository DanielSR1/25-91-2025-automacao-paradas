from django.db import models

class ParadasLinha(models.Model):
    """
    Tabela com as paradas das linhas que ainda não possuem motivo marcado.
    """
    nome_linha = models.TextField()
    inicio_parada = models.TextField()  # armazenando data/hora como texto
    fim_parada = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'paradas_linha'
        managed = False  # Django não gerencia a criação/migração da tabela

    def __str__(self):
        return f"{self.nome_linha} - {self.inicio_parada}"


class MotivosParadas(models.Model):
    """
    Tabela com as paradas que já possuem motivo marcado.
    """
    nome_linha = models.TextField()
    inicio_parada = models.TextField()  # armazenando data/hora como texto
    fim_parada = models.TextField(null=True, blank=True)
    motivo = models.TextField()

    class Meta:
        db_table = 'motivos_paradas'
        managed = False  # Django não gerencia a criação/migração da tabela

    def __str__(self):
        return f"{self.nome_linha} - {self.inicio_parada} - {self.motivo}"
