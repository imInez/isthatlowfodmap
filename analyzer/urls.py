from django.urls import path
from . import views

app_name = 'analyzer'

urlpatterns = [
    path('', views.analyze, name='analyze'),
    path('/<str:ingredients_correction>/<str:meal_url_correction>/<str:language>/', views.analyze, name='analyze'),
    path('/<str:ingredients_correction>/<str:language>/', views.analyze, name='analyze'),
    # path('search/', views.meals_search, name='meal_search')
]