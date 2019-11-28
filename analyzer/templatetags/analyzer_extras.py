from django import template
import ast

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



#not working
# @register.inclusion_tag('analyzer/safety.html')
# def safety_rate(safety_colors):
#     return safety_colors


