from django import template

register = template.Library()


@register.filter
def tipo_objeto(objeto):
    return objeto.__class__.__name__
