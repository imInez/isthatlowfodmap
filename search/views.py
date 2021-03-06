from django.contrib.postgres.search import (SearchQuery, SearchRank,
                                            SearchVector)
from django.shortcuts import render

from analyzer.utils.stemmer import stemm
from cards.models import Meal

from .forms import SearchForm


def search(request, ingredients_correction=None, meal_url_correction=None):
    meals = Meal.objects.all().order_by('-created')[0:3]
    form = SearchForm()
    query = None
    results = []
    if request.method == 'POST':
        if 'query' in request.POST:
            form = SearchForm(request.POST)
            if form.is_valid():
                query = form.cleaned_data['query']
                token = stemm(query)
                results = Meal.objects.annotate(search=SearchVector('meal_name', 'ingredients', 'tokens'),).filter(search=token[0])
                for word in token:
                    results = results | Meal.objects.annotate(search=SearchVector('meal_name', 'ingredients', 'tokens'),).filter(search=word)
    else:
        form = SearchForm()
    return render(request, 'search/search.html', {'form': form, 'query': query, 'results': results, 'meals': meals})
