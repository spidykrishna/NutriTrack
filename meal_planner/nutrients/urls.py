from django.urls import path
from . import views

urlpatterns = [
    path('nutrition/', views.nutrition_dashboard, name='nutrition_dashboard'),
    path('nutrition/goals/', views.update_goals, name='update_goals'),
    path('nutrition/log/', views.log_nutrition, name='log_nutrition'),
    path('nutrition/data/', views.get_nutrition_data, name='get_nutrition_data'),
    path('meal-plans/<int:plan_id>/analyze-nutrition/', views.analyze_meal_plan_nutrition, name='analyze_meal_plan_nutrition'),
]
