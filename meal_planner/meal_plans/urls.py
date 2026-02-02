from django.urls import path
from . import views

urlpatterns = [
    path('meal-plans/', views.meal_plan_list, name='meal_plan_list'),
    path('meal-plans/<int:pk>/', views.meal_plan_detail, name='meal_plan_detail'),
    path('meal-plans/create/', views.create_meal_plan, name='create_meal_plan'),
    path('meal-plans/<int:plan_id>/add-meal/', views.add_meal_to_plan, name='add_meal_to_plan'),
    path('meal-plans/meals/<int:meal_id>/remove/', views.remove_meal, name='remove_meal'),
    path('meal-plans/<int:plan_id>/day-meals/', views.get_day_meals, name='get_day_meals'),
    path('meal-plans/<int:plan_id>/nutrition/', views.get_meal_plan_nutrition, name='meal_plan_nutrition'),
]
