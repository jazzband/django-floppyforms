"""
This template tag library contains tools that are used in
``floppyforms/templates/*``. We don't want to expose them publicly with
``{% load floppyforms %}``.
"""
from django import template


register = template.Library()


@register.filter
def istrue(value):
    return value is True


@register.filter
def isfalse(value):
    return value is False


@register.filter
def isnone(value):
    return value is None
