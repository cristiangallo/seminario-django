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


class Genero(models.Model):
    descripcion = models.CharField(max_length=30, unique=True, verbose_name="Descripción")

    class Meta:
        verbose_name = 'Género'  # ← Podemos definir el nombre para mostrar de la clase
        verbose_name_plural = 'Géneros'  # ← Django pluraliza agregando 's' al final del nombre de la clase

    def __str__(self):
        return self.descripcion


class Libro(models.Model):
    # Los libros se identifican mediante su ISBN, tienen un título, cantidad de páginas, uno o más autores y pertenecen
    # a un género literario.
    titulo = models.CharField(max_length=50, verbose_name="Título")
    cantidad = models.IntegerField(default=0)
    genero = models.ForeignKey(Genero, on_delete=models.PROTECT, verbose_name="Género")
    autores = models.ManyToManyField(Autor, verbose_name="Autores", through='LibroAutor')

    def __str__(self):
        return self.titulo

    @property
    def isbn(self):
        isbn = str(self.id)
        return "-".join([isbn[0:3], isbn[3:4], isbn[4:6], isbn[6:12], isbn[12]])


class LibroAutor(models.Model):
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE)
    autor = models.ForeignKey(Autor, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Libros autores'

    def __str__(self):
        return "{} {}".format(self.autor, self.libro)
