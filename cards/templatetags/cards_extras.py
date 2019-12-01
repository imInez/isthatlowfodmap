import ast
import re

from django import template

from ..models import Meal

register = template.Library()
@register.filter
def cut_imgsrc(value):
    return value.replace('[', '').replace(']', '').replace(",", '').replace("'", '')

@register.filter
def evaluate_list(value):
    print('VAL: ', value, type(value))
    return ast.literal_eval(value)

@register.filter
def add_class(value, new_class):
    return value.as_widget(attrs={'class': new_class})

@register.filter
def split(value, splitter):
    return value.split(splitter)

@register.filter
def leave_ingrs(value):
    value = [line.replace('&#39;', '') for line in value]
    value[0] = value[0].split('[')[1]
    value[-1] = value[-1].split(']')[0]
    return value

@register.inclusion_tag('cards/meal/profile.html',)
def show_meals(start=0, end=6):
    meals = Meal.objects.all()[start:end]
    return {'meals': meals}
