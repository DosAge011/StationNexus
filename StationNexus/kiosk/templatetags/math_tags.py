from django import template

register = template.Library()


@register.filter
def mult(a, b):
    return a * b
