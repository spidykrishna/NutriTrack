from django.contrib import admin
from .models import MealPlan, DailyMeal

class DailyMealInline(admin.TabularInline):
    model = DailyMeal
    extra = 1

@admin.register(MealPlan)
class MealPlanAdmin(admin.ModelAdmin):
    list_display = ['name', 'start_date', 'end_date', 'total_days', 'user']
    list_filter = ['start_date', 'end_date']
    search_fields = ['name', 'description']
    inlines = [DailyMealInline]

@admin.register(DailyMeal)
class DailyMealAdmin(admin.ModelAdmin):
    list_display = ['meal_plan', 'date', 'meal_slot', 'recipe', 'servings']
    list_filter = ['meal_slot', 'date']
    search_fields = ['recipe__name']
