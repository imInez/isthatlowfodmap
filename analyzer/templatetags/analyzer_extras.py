import ast

from django import template

register = template.Library()

@register.filter(name='get_details')
def get_details(dictionary, key):
    return dictionary.get(key)


@register.filter
def nothing(value):
    if value is None or value == "None" or value == "None ":
        return ''

@register.filter
def make_range(value):
    return [x for x in range(value)]

@register.filter
def eval(value):
    try:
        return ast.literal_eval(value)
    except SyntaxError:
        return value
    except ValueError:
        return value
