from django import forms
from .models import Meal
import ast


class MealCreateForm(forms.ModelForm):
    meal_url = forms.URLField(required=False)

    class Meta:
        model = Meal
        fields = ['meal_name', 'safety', 'meal_url', 'image_file',  'ingredients',  'image_url', 'results', 'tokens' ]
        widgets = {
            # 'results': forms.TextInput(attrs={'class': 'd-none'}),
            #        'ingredients': forms.TextInput(attrs={'class': 'd-none'}),
            #        'safety': forms.TextInput(attrs={'class': 'd-none'}),
            #        'tokens': forms.TextInput(attrs={'class': 'd-none'}),
                   'image_file': forms.FileInput}
        # labels = {'results': '', 'ingredients': '', 'safety': '', 'tokens': ''}

    def clean_ingredients(self):
        cd = self.cleaned_data
        try:
            singles = [s.strip() for s in self.data.getlist('single_ingredients')]
            if len(singles) > 0:
                cd['ingredients'] = singles
        except:  # TODO what except will be caught?
            pass
        return cd['ingredients']

    def clean_results(self):
        cd = self.cleaned_data
        results = cd['results']
        ingrs = cd['ingredients']
        print("RES: ", results)
        if isinstance(results, str) and len(results)>0:
            results = ast.literal_eval(results)
        if len(ingrs) > 0:
            results = [r for r in results if r[0] in ingrs]
        return results
