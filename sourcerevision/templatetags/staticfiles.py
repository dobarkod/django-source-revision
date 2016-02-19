from django import template
from django.conf import settings
from django.templatetags.static import static as django_static
from ..loader import get_revision

register = template.Library()

__all__ = ['static']


def static(path):
    rev = get_revision()
    qs = (u'?rev=' + rev) if rev else u''
    return django_static(path) + qs


@register.simple_tag(name='static')
def do_static(path):
    return static(path)
