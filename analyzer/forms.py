from django import forms

class LanguageForm(forms.Form):
    CHOICES = [('ENG', 'English'), ('PL', 'Polski')]
    language = forms.ChoiceField(choices=CHOICES,  required=True, label='Select language: ')

class IngredientsForm(forms.Form):
    ingredients = forms.CharField(label='Ingredients: ', widget=forms.Textarea, required=False)

class LinkForm(forms.Form):
    link = forms.URLField(label='or link to the recipe: ', required=False)


