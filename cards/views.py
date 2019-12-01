from django.shortcuts import render, redirect, get_object_or_404
from .forms import MealCreateForm
from urllib import parse
from django import forms
import ast
from django.contrib.auth.decorators import login_required
from .models import Meal
from django.http import JsonResponse
from django.core import serializers
from universal.decorators import ajax_required
from django.views.decorators.http import require_POST


def slug(text, make_slug):
    if make_slug is True:
        return text.replace(' ', '-')
    else:
        return text.replace('-', ' ')


@login_required
def meal_create(request):
    meal_url = request.POST.get('meal_url')
    meal_name = slug(request.POST.get('meal_name'), False)
    ingredients = request.POST.get('ingredients')
    meal_images = slug(request.POST.get('meal_images'), False) if request.POST.get('meal_images') else None
    results = request.POST.get('results')
    safety = slug(request.POST.get('safety'), False)
    tokens = slug(request.POST.get('tokens'), False)

    ingr_table = None
    res_table = None
    data = [meal_url, meal_name, ingredients, meal_images, results]
    try:
        ingr_table = parse.unquote(slug(ingredients, False)).split('\n')
        res_table = ast.literal_eval(parse.unquote(slug(results, False)))
    except AttributeError:
        pass

    if request.method == 'POST':
        if any(item is not None for item in data):
            form = MealCreateForm()
            if meal_name != 'None':
                form.fields['meal_name'].initial = str(meal_name).replace(',', '').replace('\\n', '').replace("'",'').strip()
            if meal_url != 'None':
                form.fields['meal_url'].initial = parse.unquote(meal_url)
            form.fields['ingredients'].initial = ingr_table
            form.fields['results'].initial = res_table
            form.fields['safety'].initial = safety
            form.fields['tokens'].initial = tokens
            if meal_images != 'None' and meal_images is not None:
                meal_images = parse.unquote(meal_images).split()
                form.fields['image_file'].widget = forms.HiddenInput()
                form.fields['image_url'].widget = forms.HiddenInput()
            else:
                form.fields['image_url'].widget = forms.HiddenInput()
                meal_images = None
            if request.POST.get('save') == 'True':
                form = MealCreateForm(request.POST, request.FILES)
        else:
            form = MealCreateForm(request.POST, request.FILES)
        if form.is_valid():
            new_meal = form.save(commit=False)
            new_meal.author = request.user
            new_meal.save()
            new_meal.collectors.add(request.user)
            return redirect(new_meal.get_absolute_url())
    else:
        form = MealCreateForm()
    return render(request, 'cards/meal/create.html',
                  {'form': form, 'meal_images': meal_images, 'ingr_table': ingr_table,
                   'res_table': res_table, 'safety': safety})


def meal_details(request, id):
    meal = get_object_or_404(Meal, id=id)
    ingredients = ast.literal_eval(meal.ingredients)
    results = ast.literal_eval(parse.unquote(slug(meal.results, False)))
    safety = ast.literal_eval(meal.safety)
    is_author = True if meal.author == request.user else False
    return render(request, 'cards/meal/details.html',
                  {'meal': meal, 'results': results, 'ingredients': ingredients,
                   'safety': safety, 'is_author': is_author})


def meals_list(request):
    start = int(request.GET.get('start', 3))
    end = int(request.GET.get('end', 5))
    meals =  Meal.objects.all().order_by('-created')[start:end]
    data = serializers.serialize('json', meals,
                                 fields=('meal_name', 'meal_url', 'safety', 'image_file', 'image_url', 'safety'))
    return JsonResponse(data, safe=False)


@ajax_required
@login_required()
@require_POST
def collect(request):
    meal_id = request.POST.get('id')
    action = request.POST.get('action')
    if meal_id and action:
        try:
            meal = Meal.objects.get(id=meal_id)
            if action == 'add':
                meal.collectors.add(request.user)
            else:
                meal.collectors.remove(request.user)
        except:
            pass
    return JsonResponse({'status': 'ok'})


def edit(request, pk):
    this_meal = Meal.objects.filter(pk=pk).first()
    if request.method == 'POST':
        form = MealCreateForm(instance=this_meal, data=request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            form.save()
            return redirect(this_meal.get_absolute_url())
    else:
        form = MealCreateForm(instance=this_meal)
    return render(request, 'cards/meal/meal_edit.html', {'form': form, 'meal': this_meal})
