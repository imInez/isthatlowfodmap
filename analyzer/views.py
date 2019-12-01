from django.shortcuts import render
from .forms import IngredientsForm, LinkForm, LanguageForm
from search.forms import SearchForm
from .utils.ingredients_checker import IngredientsChecker
from .utils.scraper import Scraper
from .utils.safety import calculate_safety
from .utils.stemmer import stemm
from urllib import parse
from cards.models import Meal
from django.contrib.postgres.search import SearchVector


def slug(text, make_slug):
    if make_slug is True:
        return text.replace(' ', '-')
    else:
        return text.replace('-', ' ')


def get_website_data(link_form):
        scraper = Scraper()
        meal = scraper.parse(link_form['link'].value())
        meal_name = slug(str(meal.name).replace(',', '').replace('/\n', '').replace("'", '').strip(), True)
        meal_url = parse.quote(meal.url, safe='')
        meal_images = slug(str([parse.quote(img, safe='') for img in meal.images]), True)

        return {'meal': meal, 'meal_name': meal_name, 'meal_url': meal_url, 'meal_images': meal_images}


def get_results(ingredients, language):
    checker = IngredientsChecker(ingredients)
    results, not_found, ingredients, stems = checker.check_ingredients(language)
    stems = slug(str(stems), True)
    print('INGR: ', ingredients)
    print('RES: ', results)
    safety = slug(str(calculate_safety(results)), True)
    return {'results': results, 'not_found': not_found, 'ingredients': ingredients, 'stems': stems, 'safety': safety}


def analyze(request, ingredients_correction=None, meal_url_correction=None, language=None):
    meals = Meal.objects.all().order_by('-created')[0:3]
    search_form = SearchForm()
    meal_data = dict()
    results_data = dict()
    ingredients_save, results_save= None, None
    language = request.POST.get('language') if not language or request.POST.get('language') != language else language
    if request.method == 'POST':
        language_form = LanguageForm(request.POST)
        ingr_form = IngredientsForm(request.POST)
        link_form = LinkForm(request.POST)
        if ingr_form.data['ingredients']:
            if ingr_form.is_valid():
                if link_form.data['link']:
                    meal_data = get_website_data(link_form)
                results_data = get_results(ingr_form['ingredients'].value(), language)
        elif link_form.data['link']:
            if link_form.is_valid():
                meal_data = get_website_data(link_form)
                results_data = get_results(meal_data['meal'].ingredients.split('\n'), language)
        if results_data:
            results_save = parse.quote(slug(str(results_data.get('results')), True), safe='')
            ingredients_save = parse.quote(slug('\n'.join(results_data.get('ingredients', '')), True), safe='')
    else:
        language_form = LanguageForm()
        ingr_form = IngredientsForm()
        link_form = LinkForm()
        if ingredients_correction:
            ingr_form.fields['ingredients'].initial = parse.unquote(slug(ingredients_correction, False))
            if meal_url_correction and meal_url_correction != "None":
                link_form.fields['link'].initial = parse.unquote(meal_url_correction)
            language_form.fields['language'].initial = language
    return render(request, 'analyzer/analyze.html',
                  {'language_form': language_form, 'ingr_form': ingr_form, 'link_form': link_form, 'language': language,
                   #this is for results table
                   'ingredients': results_data.get('ingredients', None),
                   'results': results_data.get('results', None), 'not_found': results_data.get('not_found', None),
                   # this is for saving form
                   'meal_name': meal_data.get('meal_name', None), 'meal_url': meal_data.get('meal_url', None),
                   'meal_images': meal_data.get('meal_images', None),
                   'ingredients_save': ingredients_save, 'results_save': results_save,
                   'meals': meals, 'safety': results_data.get('safety', None),
                   'tokens': results_data.get('stems', None),
                   'search_form': search_form })


def meals_search(request):
    form = SearchForm()
    query = None
    results = []
    print("MEALS SEARCH")
    if 'query' in request.GET:
        print('QUERY: ', query)
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            token = stemm(query)
            print('TOKEN: ', token, type(token))
            results = Meal.objects.annotate(search=SearchVector('meal_name', 'ingredients', 'tokens'),).filter(search=token[0])
            for word in token:
                results = results | Meal.objects.annotate(search=SearchVector('meal_name', 'ingredients', 'tokens'),).filter(search=word)
    return render(request, 'analyzer/search.html', {'form': form, 'query': query, 'results': results})




