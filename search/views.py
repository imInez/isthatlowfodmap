from django.shortcuts import render
from cards.models import Meal
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from .forms import SearchForm
from analyzer.utils.stemmer import stemm

def search(request, ingredients_correction=None, meal_url_correction=None):
    print('SEARCH VIEW')
    meals = Meal.objects.all().order_by('-created')[0:3]
    form = SearchForm()
    query = None
    results = []
    print("MEALS SEARCH")
    if request.method == 'POST':
        if 'query' in request.POST:
            print('QUERY: ', request.POST.get('query'))
            form = SearchForm(request.POST)
            if form.is_valid():
                query = form.cleaned_data['query']
                token = stemm(query)
                print('TOKEN: ', token, type(token))
                results = Meal.objects.annotate(search=SearchVector('meal_name', 'ingredients', 'tokens'),).filter(search=token[0])
                for word in token:
                    results = results | Meal.objects.annotate(search=SearchVector('meal_name', 'ingredients', 'tokens'),).filter(search=word)
    else:
        form = SearchForm()
    return render(request, 'search/search.html', {'form': form, 'query': query, 'results': results, 'meals': meals})


