# -*- coding: UTF-8 -*-

from django.contrib import admin
from singleton.admin import SingletonModelAdmin
from .models import Configuracion, Libro, Autor, Genero, Socio, Bibliotecario, Prestamo


@admin.register(Configuracion)
class ConfiguracionAdmin(SingletonModelAdmin):
    # Configuracion.load()
    pass

@admin.register(Libro)
class LibroAdmin(admin.ModelAdmin):
    pass


@admin.register(Autor)
class AutorAdmin(admin.ModelAdmin):
    pass


@admin.register(Genero)
class GeneroAdmin(admin.ModelAdmin):
    pass

admin.site.register(Socio)

admin.site.register(Bibliotecario)

admin.site.register(Prestamo)