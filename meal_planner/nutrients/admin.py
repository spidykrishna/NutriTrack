from django.contrib import admin
from .models import NutritionGoal, NutritionLog

@admin.register(NutritionGoal)
class NutritionGoalAdmin(admin.ModelAdmin):
    list_display = ['user', 'daily_calories', 'daily_protein', 'daily_carbs', 'daily_fats']
    search_fields = ['user__username']

@admin.register(NutritionLog)
class NutritionLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'date', 'calories_consumed', 'protein_consumed', 'carbs_consumed', 'fats_consumed']
    list_filter = ['date']
    search_fields = ['user__username', 'notes']
    date_hierarchy = 'date'
