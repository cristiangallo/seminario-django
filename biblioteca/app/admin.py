# -*- coding: UTF-8 -*-

from django.contrib import admin
from singleton.admin import SingletonModelAdmin
from .models import (
    Configuracion, Libro, Autor, Genero, Socio, Bibliotecario, Prestamo, LibroAutor, Ejemplar)  # , PrestamoPendiente


admin.site.register(Ejemplar)

@admin.register(Configuracion)
class ConfiguracionAdmin(SingletonModelAdmin):
    # Configuracion.load()
    pass


class LibroAutorInline(admin.StackedInline):
    model = LibroAutor
    extra = 0


@admin.register(Libro)
class LibroAdmin(admin.ModelAdmin):
    # filter_horizontal = ('autores',)
    inlines = [LibroAutorInline]

@admin.register(Autor)
class AutorAdmin(admin.ModelAdmin):
    pass


@admin.register(Genero)
class GeneroAdmin(admin.ModelAdmin):
    pass

admin.site.register(Socio)

admin.site.register(Bibliotecario)

admin.site.register(Prestamo)


# @admin.register(PrestamoPendiente)
# class PrestamoPendienteAdmin(admin.ModelAdmin):
#     def get_queryset(self, request):
#         # un libro no está devuelto cuando no tiene fecha de devolución
#         return super().get_queryset(request).filter(fecha_dev__isnull=True)