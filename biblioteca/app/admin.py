# -*- coding: UTF-8 -*-

from django.contrib import admin
from singleton.admin import SingletonModelAdmin
from .models import (
    Configuracion, Libro, Autor, Genero, Socio, Bibliotecario, Prestamo, LibroAutor, Ejemplar, PrestamoPendiente)


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

@admin.register(Socio)
class SocioAdmin(admin.ModelAdmin):
    from .forms import SocioForm
    form = SocioForm


admin.site.register(Bibliotecario)


@admin.register(Prestamo)
class PrestamoAdmin(admin.ModelAdmin):
    list_display = ["id", "socio", "ejemplar", "entrego", "recibio", "fecha_max_dev", "fecha_dev"]


@admin.register(PrestamoPendiente)
class PrestamoPendienteAdmin(PrestamoAdmin):
    search_fields = ('socio__dni__startswith',)

    def get_queryset(self, request):
        return super(PrestamoPendienteAdmin, self).get_queryset(request).filter(recibio__isnull=True)
