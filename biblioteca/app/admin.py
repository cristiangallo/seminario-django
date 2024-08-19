# -*- coding: UTF-8 -*-

from django.contrib import admin
from singleton.admin import SingletonModelAdmin
from .models import Configuracion


@admin.register(Configuracion)
class ConfiguracionAdmin(SingletonModelAdmin):
    # Configuracion.load()
    pass