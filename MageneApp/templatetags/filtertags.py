from django import template
import math

register = template.Library()


@register.filter(name='modulo')
def modulo(num, val):
    return num % val


@register.filter
def nonestr(value):
    if value is None:
        ret = ''
    else:
        ret = value
    return ret


@register.filter
def addval(num, val):
      return num+val

@register.filter
def addsqrtval(num, val):
      return num*1.5/10

@register.filter
def addtrestval(num, val):
      return num*3+val
