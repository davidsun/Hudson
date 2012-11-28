#-*- coding:utf-8 -*-

from django import template
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

from sns.libs.utils import filter_at_users, at_users


register = template.Library()

@register.filter
def at_users(content, autoescape=None):
    if autoescape:
        esca = conditional_escape
    else:
        esca = lambda x: x
    filtered = filter_at_users(esca(content))
    return mark_safe(filtered)

at_users.needs_autoescape = True
