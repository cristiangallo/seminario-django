# -*- coding: UTF-8 -*-

"""
:author: Cristián M. Gallo (mail@cristiangallo.com.ar)
"""

from django.contrib import admin


class SingletonModelAdmin(admin.ModelAdmin):
    actions = None

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False
