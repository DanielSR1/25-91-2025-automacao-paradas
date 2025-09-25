from django.db import models

class ParadasLinha(models.Model):
    nome_linha = models.TextField()
    inicio_parada = models.TextField()
    fim_parada = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'paradas_linha'
        managed = False



class MotivosParadas(models.Model):
    nome_linha = models.TextField()
    inicio_parada = models.TextField()
    fim_parada = models.TextField(null=True, blank=True)
    motivo = models.TextField()

    class Meta:
        db_table = 'motivos_paradas'
        managed = False
