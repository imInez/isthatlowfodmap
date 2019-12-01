from django.urls import include, path

from . import views

app_name = 'cards'

urlpatterns = [

    path('create/?meal_name=<str:meal_name>/?meal_url=<str:meal_url>/?ingredients=<str:ingredients>/?results=<results>/?meal_images=<meal_images>/?safety=<safety>/?tokens=<str:tokens>/',
         views.meal_create, name='meal_create'),
    path('create/', views.meal_create, name='meal_create'),
    path('details/<int:id>/', views.meal_details, name='meal_details'),
    path('edit/<int:pk>/', views.edit, name='meal_edit'),
    path('meals_list/', views.meals_list, name='meals_list'),
    path('collect/', views.collect, name='collect')


]
