from django import template

from ..utils import category_dict

register = template.Library()


@register.filter
def translate_(key):
    return category_dict.get(key)