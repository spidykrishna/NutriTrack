from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from .models import ShoppingList, ShoppingListItem
from meal_plans.models import MealPlan
from recipes.models import Ingredient
import json

def shopping_list_detail(request, pk=None):
    """Show shopping list details"""
    if pk:
        shopping_list = get_object_or_404(ShoppingList, pk=pk)
    else:
        
        shopping_list = ShoppingList.objects.first()
        if not shopping_list:
            shopping_list = ShoppingList.objects.create(name="My Shopping List")
    
    items = shopping_list.items.all()
    
    
    items_by_category = {}
    for item in items:
        
        if item.ingredient and item.ingredient.category:
            cat_name = str(item.ingredient.category)
        else:
            cat_name = 'Other'

            
        if cat_name not in items_by_category:
            items_by_category[cat_name] = []
        items_by_category[cat_name].append(item)
    
    context = {
        'shopping_list': shopping_list,
        'items_by_category': items_by_category,
        'purchased_count': items.filter(purchased=True).count(),
        'total_count': items.count(),
    }
    return render(request, 'shopping_list/shopping_list_detail.html', context)

def generate_shopping_list(request, plan_id):
    """Generate shopping list from meal plan"""
    meal_plan = get_object_or_404(MealPlan, pk=plan_id)
    
    shopping_list, created = ShoppingList.objects.get_or_create(
        meal_plan=meal_plan,
        defaults={'name': f'Shopping List for {meal_plan.name}'}
    )
    
    shopping_list.generate_from_meal_plan()
    return redirect('shopping_list_detail', pk=shopping_list.id)

@csrf_exempt
@require_POST
def add_custom_item(request, list_id):
    """Add a custom item to shopping list"""
    shopping_list = get_object_or_404(ShoppingList, pk=list_id)
    
    try:
        data = json.loads(request.body)
        name = data.get('name')
        
        if not name or not name.strip():
            return JsonResponse({'success': False, 'error': 'Item ka naam likh pehle!'}, status=400)

        
        try:
            amount_val = float(data.get('amount', 1))
        except (TypeError, ValueError):
            amount_val = 1.0

        
        ingredient, created = Ingredient.objects.get_or_create(
            name=name.strip(),
            defaults={
                'calories': 0, 'protein': 0, 'carbs': 0, 'fats': 0,
            }
        )
        
        
        item = ShoppingListItem.objects.create(
            shopping_list=shopping_list,
            ingredient=ingredient,
            amount=amount_val,
            unit=data.get('unit', 'piece'),
            purchased=False
        )
        
        return JsonResponse({
            'success': True,
            'item_id': item.id,
            'item_name': item.ingredient.name,
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

@csrf_exempt
@require_POST
def toggle_item_purchased(request, item_id):
    """Toggle purchased status of an item"""
    item = get_object_or_404(ShoppingListItem, pk=item_id)
    item.purchased = not item.purchased
    item.save()
    
    return JsonResponse({
        'success': True,
        'purchased': item.purchased
    })

@csrf_exempt
@require_POST
def update_item_amount(request, item_id):
    """Update item amount"""
    item = get_object_or_404(ShoppingListItem, pk=item_id)
    data = json.loads(request.body)
    item.amount = data.get('amount', item.amount)
    item.save()
    return JsonResponse({'success': True, 'amount': item.amount})

@csrf_exempt
@require_POST
def remove_item(request, item_id):
    """Remove an item from shopping list"""
    item = get_object_or_404(ShoppingListItem, pk=item_id)
    item.delete()
    return JsonResponse({'success': True})

@csrf_exempt
@require_POST
def clear_purchased(request, list_id):
    """Remove all purchased items"""
    shopping_list = get_object_or_404(ShoppingList, pk=list_id)
    shopping_list.items.filter(purchased=True).delete()
    return JsonResponse({'success': True})

def shopping_lists(request):
    """List all shopping lists"""
    lists = ShoppingList.objects.all().order_by('-created_at')
    return render(request, 'shopping_list/shopping_lists.html', {'shopping_lists': lists})

@csrf_exempt
@require_POST
def clear_all_items(request, list_id):
    shopping_list = get_object_or_404(ShoppingList, id=list_id)
    shopping_list.items.all().delete()
    return JsonResponse({"success": True})