from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from .models import NutritionGoal, NutritionLog
from meal_plans.models import MealPlan
import json
from datetime import datetime, timedelta

def nutrition_dashboard(request):
    """Main nutrition dashboard"""
    
    goals, created = NutritionGoal.objects.get_or_create(
        user=None,  
        defaults={
            'daily_calories': 2000,
            'daily_protein': 150,
            'daily_carbs': 250,
            'daily_fats': 70,
            'daily_fiber': 30,
        }
    )
    
    
    today = timezone.now().date()
    log, created = NutritionLog.objects.get_or_create(
        user=None,
        date=today,
        defaults={
            'calories_consumed': 0,
            'protein_consumed': 0,
            'carbs_consumed': 0,
            'fats_consumed': 0,
            'fiber_consumed': 0,
        }
    )
    
    
    week_start = today - timedelta(days=7)
    weekly_logs = NutritionLog.objects.filter(
        user=None,
        date__gte=week_start,
        date__lte=today
    ).order_by('date')
    
    context = {
        'goals': goals,
        'today_log': log,
        'comparison': log.compare_with_goals(goals),
        'weekly_logs': weekly_logs,
    }
    return render(request, 'nutrients/nutrition_dashboard.html', context)

@csrf_exempt
def update_goals(request):
    """Update nutrition goals"""
    goals, created = NutritionGoal.objects.get_or_create(
        user=None,
        defaults={
            'daily_calories': 2000,
            'daily_protein': 150,
            'daily_carbs': 250,
            'daily_fats': 70,
            'daily_fiber': 30,
        }
    )
    
    if request.method == 'POST':
        data = json.loads(request.body)
        
        goals.daily_calories = data.get('daily_calories', goals.daily_calories)
        goals.daily_protein = data.get('daily_protein', goals.daily_protein)
        goals.daily_carbs = data.get('daily_carbs', goals.daily_carbs)
        goals.daily_fats = data.get('daily_fats', goals.daily_fats)
        goals.daily_fiber = data.get('daily_fiber', goals.daily_fiber)
        
        goals.protein_percentage = data.get('protein_percentage', goals.protein_percentage)
        goals.carbs_percentage = data.get('carbs_percentage', goals.carbs_percentage)
        goals.fats_percentage = data.get('fats_percentage', goals.fats_percentage)
        
        goals.save()
        
        return JsonResponse({'success': True})
    
    return JsonResponse({
        'daily_calories': goals.daily_calories,
        'daily_protein': goals.daily_protein,
        'daily_carbs': goals.daily_carbs,
        'daily_fats': goals.daily_fats,
        'daily_fiber': goals.daily_fiber,
        'protein_percentage': goals.protein_percentage,
        'carbs_percentage': goals.carbs_percentage,
        'fats_percentage': goals.fats_percentage,
    })

@csrf_exempt
def log_nutrition(request):
    """Log nutrition for today"""
    if request.method == 'POST':
        data = json.loads(request.body)
        
        today = timezone.now().date()
        log, created = NutritionLog.objects.get_or_create(
            user=None,
            date=today,
            defaults={
                'calories_consumed': 0,
                'protein_consumed': 0,
                'carbs_consumed': 0,
                'fats_consumed': 0,
                'fiber_consumed': 0,
            }
        )
        
       
        log.calories_consumed += data.get('calories', 0)
        log.protein_consumed += data.get('protein', 0)
        log.carbs_consumed += data.get('carbs', 0)
        log.fats_consumed += data.get('fats', 0)
        log.fiber_consumed += data.get('fiber', 0)
        log.save()
        
        return JsonResponse({
            'success': True,
            'log': {
                'calories': log.calories_consumed,
                'protein': log.protein_consumed,
                'carbs': log.carbs_consumed,
                'fats': log.fats_consumed,
                'fiber': log.fiber_consumed,
            }
        })
    
    return JsonResponse({'success': False})

def get_nutrition_data(request):
    """Get nutrition data for a date range"""
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    
    logs = NutritionLog.objects.filter(user=None)
    
    if start_date:
        logs = logs.filter(date__gte=start_date)
    if end_date:
        logs = logs.filter(date__lte=end_date)
    
    data = [{
        'date': log.date.strftime('%Y-%m-%d'),
        'calories': log.calories_consumed,
        'protein': log.protein_consumed,
        'carbs': log.carbs_consumed,
        'fats': log.fats_consumed,
        'fiber': log.fiber_consumed,
    } for log in logs.order_by('date')]
    
    return JsonResponse({'data': data})

def analyze_meal_plan_nutrition(request, plan_id):
    """Analyze nutrition for a meal plan"""
    meal_plan = get_object_or_404(MealPlan, pk=plan_id)
    
    
    goals, _ = NutritionGoal.objects.get_or_create(
        user=None,
        defaults={
            'daily_calories': 2000,
            'daily_protein': 150,
            'daily_carbs': 250,
            'daily_fats': 70,
            'daily_fiber': 30,
        }
    )
    
    daily_nutrition = {}
    for meal in meal_plan.dailymeal_set.all():
        date_str = meal.date.strftime('%Y-%m-%d')
        if date_str not in daily_nutrition:
            daily_nutrition[date_str] = {
                'calories': 0, 'protein': 0, 'carbs': 0, 'fats': 0, 'fiber': 0
            }
        
        nutrition = meal.nutrition
        for key in daily_nutrition[date_str]:
            daily_nutrition[date_str][key] += nutrition.get(key, 0)
    
    
    analysis = {}
    for date, nutrition in daily_nutrition.items():
        analysis[date] = {
            'nutrition': {k: round(v, 2) for k, v in nutrition.items()},
            'vs_goals': {
                'calories': round((nutrition['calories'] / goals.daily_calories) * 100, 1),
                'protein': round((nutrition['protein'] / goals.daily_protein) * 100, 1),
                'carbs': round((nutrition['carbs'] / goals.daily_carbs) * 100, 1),
                'fats': round((nutrition['fats'] / goals.daily_fats) * 100, 1),
                'fiber': round((nutrition['fiber'] / goals.daily_fiber) * 100, 1),
            }
        }
    
    return JsonResponse({
        'daily_analysis': analysis,
        'goals': {
            'daily_calories': goals.daily_calories,
            'daily_protein': goals.daily_protein,
            'daily_carbs': goals.daily_carbs,
            'daily_fats': goals.daily_fats,
            'daily_fiber': goals.daily_fiber,
        }
    })
