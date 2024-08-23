# -*- coding: UTF-8 -*-

"""
:author: Cristián M. Gallo (mail@cristiangallo.com.ar)
"""

from django.db import models


class SingletonModel(models.Model):
    class Meta:
        abstract = True

    def delete(self, *args, **kwargs):
        pass

    def set_cache(self):
        from django.core.cache import cache
        cache.set(self.__class__.__name__, self)

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)
        self.set_cache()

    @classmethod
    def load(cls):
        from django.core.cache import cache
        if cache.get(cls.__name__) is None:
            obj, created = cls.objects.get_or_create(pk=1)
            if not created:
                obj.set_cache()
        return cache.get(cls.__name__)
