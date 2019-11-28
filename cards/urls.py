from django.urls import path, include
from . import views

app_name = 'cards'

urlpatterns = [
    # ?results_save=<str:results_save>/?meal_images=<meal_images>/
    path('create/?meal_name=<str:meal_name>/?meal_url=<str:meal_url>/?ingredients=<str:ingredients>/?results=<results>/?meal_images=<meal_images>/?safety=<safety>/?tokens=<str:tokens>/',
         views.meal_create, name='meal_create'),
    # path('create/<ingredients>/<meal_url>/', views.meal_create, name='meal_create'),
    path('create/', views.meal_create, name='meal_create'),
    path('details/<int:id>/', views.meal_details, name='meal_details'),
    path('edit/<int:pk>/', views.edit, name='meal_edit'),
    # path('image/', views.image, name='meal_image'),
    path('meals_list/', views.meals_list, name='meals_list'),
    # path('list/', views.list, name='list'),
    path('collect/', views.collect, name='collect')


]



# from django.urls import path, include
# from . import views
#
# app_name = 'cards'
#
# urlpatterns = [
#     # path('create/', views.meal_create_post, name='meal_create_post'),
#     # path('create/?meal_name=<str:meal_name>/?meal_url=<str:meal_url>/?ingredients_save=<str:ingredients_save>/?results_save=<str:results_save>/',
#          # ?meal_images=<meal_images>/?safety=<safety>/',
#          # views.meal_create, name='meal_create'),
#     # path('create/?ingredients_save=<str:ingredients_save>/?results_save=<str:results_save>/', views.meal_create, name='meal_create'),
# path('create/?ingredients=<str:ingredients>/?results=<str:results>/', views.meal_create, name='meal_create'),
#     path('create/', views.meal_create, name='meal_create'),
#     path('details/<int:id>/', views.meal_details, name='meal_details'),
#     # path('image/', views.image, name='meal_image'),
#
#
# ]
