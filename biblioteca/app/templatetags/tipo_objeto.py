from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def tipo_objeto(objeto):
    return objeto.__class__.__name__


@register.filter
def mensaje_busqueda(objetos):
    """
    Devuelve un safe string con la leyenda del resultado de la búsqueda
    :param objetos: queryset con resultado de búsquedas
    :return: "x objeto/s encontrado/s" alarmado con bootstrap alert
    """
    objeto = objetos.first()
    cantidad = objetos.count()
    if cantidad > 0:
        return mark_safe('<div class="alert alert-success" role="alert"><strong>{}</strong> {} {}.</div>'.format(
            cantidad,
            objeto.__class__._meta.verbose_name_plural if cantidad > 1 else objeto.__class__.__meta.verbose_name,
            'encontrados' if cantidad > 1 else 'encontrado'))

    return mark_safe(
        '<div class="alert alert-danger" role="alert"><strong>No se encontraron registros</strong> que satisfagan el '
        'criterio de búsqueda.</div>')
