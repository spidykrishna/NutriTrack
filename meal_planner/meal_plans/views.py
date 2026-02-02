from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils import timezone
from .models import MealPlan, DailyMeal
from recipes.models import Recipe
import json
from datetime import datetime, timedelta

def meal_plan_list(request):
    """List all meal plans"""
    meal_plans = MealPlan.objects.all().order_by('-created_at')
    
    context = {
        'meal_plans': meal_plans,
    }
    return render(request, 'meal_plans/meal_plan_list.html', context)

def meal_plan_detail(request, pk):
    """Show meal plan details with calendar view"""
    meal_plan = get_object_or_404(MealPlan, pk=pk)
    daily_meals = meal_plan.dailymeal_set.all()
    
    
    meals_by_date = {}
    for meal in daily_meals:
        date_str = meal.date.strftime('%Y-%m-%d')
        if date_str not in meals_by_date:
            meals_by_date[date_str] = {}
        meals_by_date[date_str][meal.meal_slot] = meal
    
    
    total_nutrition = {'calories': 0, 'protein': 0, 'carbs': 0, 'fats': 0, 'fiber': 0}
    for meal in daily_meals:
        nutrition = meal.nutrition
        for key in total_nutrition:
            total_nutrition[key] += nutrition.get(key, 0)
    
    context = {
        'meal_plan': meal_plan,
        'meals_by_date': meals_by_date,
        'total_nutrition': total_nutrition,
        'meal_slots': DailyMeal.MEAL_SLOT_CHOICES,
    }
    return render(request, 'meal_plans/meal_plan_detail.html', context)

from django.views.decorators.csrf import csrf_exempt
from datetime import datetime

@csrf_exempt
def create_meal_plan(request):
    """Create a new meal plan"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            
            start_date_str = data.get('start_date')
            end_date_str = data.get('end_date')
            
            if start_date_str:
                start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            else:
                from django.utils import timezone
                start_date = timezone.now().date()
            
            if end_date_str:
                end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
            else:
                from django.utils import timezone
                end_date = timezone.now().date() + timedelta(days=7)
            
            meal_plan = MealPlan.objects.create(
                name=data.get('name', 'New Meal Plan'),
                description=data.get('description', ''),
                start_date=start_date,
                end_date=end_date,
            )
            
            return JsonResponse({
                'success': True,
                'meal_plan_id': meal_plan.id,
                'redirect_url': f'/meal-plans/{meal_plan.id}/'
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=400)
    
    return render(request, 'meal_plans/create_meal_plan.html')

@csrf_exempt
def add_meal_to_plan(request, plan_id):
    """Add a meal to the plan"""
    meal_plan = get_object_or_404(MealPlan, pk=plan_id)
    
    if request.method == 'POST':
        data = json.loads(request.body)
        
        daily_meal = DailyMeal.objects.create(
            meal_plan=meal_plan,
            date=data.get('date'),
            meal_slot=data.get('meal_slot'),
            recipe_id=data.get('recipe_id'),
            servings=data.get('servings', 1),
            notes=data.get('notes', ''),
        )
        
        return JsonResponse({
            'success': True,
            'meal_id': daily_meal.id,
            'nutrition': daily_meal.nutrition
        })
    
    
    recipes = Recipe.objects.all()
    
    context = {
        'meal_plan': meal_plan,
        'recipes': recipes,
        'meal_slots': DailyMeal.MEAL_SLOT_CHOICES,
    }
    return render(request, 'meal_plans/add_meal.html', context)

@csrf_exempt
def remove_meal(request, meal_id):
    """Remove a meal from the plan"""
    meal = get_object_or_404(DailyMeal, pk=meal_id)
    plan_id = meal.meal_plan.id
    meal.delete()
    
    return JsonResponse({'success': True})

def get_day_meals(request, plan_id):
    """Get meals for a specific day"""
    meal_plan = get_object_or_404(MealPlan, pk=plan_id)
    date = request.GET.get('date')
    
    meals = DailyMeal.objects.filter(
        meal_plan=meal_plan,
        date=date
    ).select_related('recipe')
    
    meals_data = []
    for meal in meals:
        meals_data.append({
            'id': meal.id,
            'meal_slot': meal.meal_slot,
            'meal_slot_display': meal.get_meal_slot_display(),
            'recipe_name': meal.recipe.name,
            'recipe_id': meal.recipe.id,
            'servings': meal.servings,
            'nutrition': meal.nutrition,
        })
    
    return JsonResponse({'meals': meals_data})

def get_meal_plan_nutrition(request, plan_id):
    """Get total nutrition for a meal plan"""
    meal_plan = get_object_or_404(MealPlan, pk=plan_id)
    
    total_nutrition = {'calories': 0, 'protein': 0, 'carbs': 0, 'fats': 0, 'fiber': 0}
    for meal in meal_plan.dailymeal_set.all():
        nutrition = meal.nutrition
        for key in total_nutrition:
            total_nutrition[key] += nutrition.get(key, 0)
    
   
    total_nutrition = {k: round(v, 2) for k, v in total_nutrition.items()}
    
    return JsonResponse(total_nutrition)
def create_meal_plan(request):
    
    return render(request, 'meal_plans/create_meal_plan.html')