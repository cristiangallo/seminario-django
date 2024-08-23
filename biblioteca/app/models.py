# -*- coding: UTF-8 -*-
from django.contrib.auth.models import User
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
    cant_pag = models.IntegerField(default=0, verbose_name="Cant. de páginas")
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


class Ejemplar(models.Model):
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE)
    nro_ejemplar = models.IntegerField(default=1)

    def __str__(self):
        return "{}-{}".format(self.nro_ejemplar, self.libro)


class Socio(models.Model):
    dni = models.CharField(max_length=10, verbose_name="DNI", unique=True)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    direccion = models.CharField(max_length=50)
    telefono = models.CharField(max_length=10, null=True, blank=True)
    celular = models.CharField(max_length=10, null=True, blank=True)
    fecha_nacimiento = models.DateField()

    def __str__(self):
        return "{}, {}".format(self.apellido, self.nombre)


class Bibliotecario(Socio):
    desde = models.DateTimeField(auto_now_add=True)
    usuario = models.OneToOneField(User, on_delete=models.PROTECT)


class Prestamo(models.Model):
    ejemplar = models.ForeignKey(Ejemplar, on_delete=models.PROTECT)
    socio = models.ForeignKey(Socio, on_delete=models.PROTECT)
    entrego = models.ForeignKey(Bibliotecario, on_delete=models.PROTECT, related_name='entrego')
    recibio = models.ForeignKey(Bibliotecario, on_delete=models.PROTECT, related_name='recibio', null=True, blank=True)
    fecha_max_dev = models.DateField(
        verbose_name="Fecha máxima de devolución", help_text="El socio debe devolver el libro antes de esta fecha.")
    fecha_dev = models.DateField(verbose_name="Fecha de devolución", null=True, blank=True)

    def __str__(self):
        return "{}".format(self.id)


class PrestamoPendiente(Prestamo):

    class Meta:
        proxy = True


# Implementamos patrón Singleton para la configuración del sistema
# Singleton es un patrón de diseño creacional que nos permite asegurarnos de que una clase tenga una única instancia,
# a la vez que proporciona un punto de acceso global a dicha instancia
from singleton.models import SingletonModel
class Configuracion(SingletonModel):
    plazo_max_devolucion = models.IntegerField(
        default=3, verbose_name="Plazo máximo de devolución",
        help_text="Expresado en días"
    )
    cant_max_prest_act = models.IntegerField(default=3, verbose_name="Cant. máxima de préstamos activos")

    class Meta:
        verbose_name, verbose_name_plural = "Configuración", "Configuraciones"

    def __str__(self):
        return "Configuración sistema Biblioteca"
