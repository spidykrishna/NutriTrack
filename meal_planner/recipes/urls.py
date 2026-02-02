from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('recipes/', views.recipe_list, name='recipe_list'),
    path('recipes/<int:pk>/', views.recipe_detail, name='recipe_detail'),
    path('recipes/search/', views.search_recipes, name='search_recipes'),
    path('recipes/protein-sources/', views.protein_sources, name='protein_sources'),
    path('ingredients/<int:ingredient_id>/alternatives/', views.get_protein_alternatives, name='protein_alternatives'),
]
