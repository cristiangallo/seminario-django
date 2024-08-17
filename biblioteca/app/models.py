# -*- coding: UTF-8 -*-

from django.db import models


# app.models.py
class Autor(models.Model):
    # Los autores se identifican por un id secuencial y se registra de ellos una descripción
    # compuesta por su pseudónimo o nombre y apellido.

    # id = models.BigIntegerField(primary_key=True)  <--Django lo hace en forma predeterminada
    nombre = models.CharField(max_length=30, null=True, blank=True)
    apellido = models.CharField(max_length=30, null=True, blank=True)
    pseudonimo = models.CharField(max_length=30, verbose_name='Pseudónimo', null=True, blank=True)
    modificado = models.DateTimeField(auto_now=True)
    creado = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Autores'
        # db_table = 'autores' por defecto app_name_classname en este caso app_autor

    def __str__(self):
        return self.pseudonimo if self.pseudonimo else "{} {}".format(self.nombre, self.apellido)
