# yourapp/templatetags/custom_filters.py
from django import template

register = template.Library()

@register.filter
def split_string(value, delimiter=":"):
    """Splits a string by the specified delimiter."""
    if delimiter in value:
        return value.split(delimiter, 1)
    return [value, ""]

