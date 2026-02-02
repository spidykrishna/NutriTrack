from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from .models import Recipe, Ingredient, Category, ProteinAlternative
import json

def home(request):
    """Home page with featured recipes"""
    featured_recipes = Recipe.objects.all()[:6]
    categories = Category.objects.all()
    
    context = {
        'featured_recipes': featured_recipes,
        'categories': categories,
    }
    return render(request, 'recipes/home.html', context)

def recipe_list(request):
    """List all recipes with filtering"""
    recipes = Recipe.objects.all()
    
    
    meal_type = request.GET.get('meal_type')
    if meal_type:
        recipes = recipes.filter(meal_type=meal_type)
    
    
    difficulty = request.GET.get('difficulty')
    if difficulty:
        recipes = recipes.filter(difficulty=difficulty)
    
    
    category = request.GET.get('category')
    if category:
        recipes = recipes.filter(categories__id=category)
    
    
    search_query = request.GET.get('q')
    if search_query:
        recipes = recipes.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(tags__icontains=search_query)
        )
    
    
    protein_source = request.GET.get('protein_source')
    if protein_source:
        recipes = recipes.filter(
            recipeingredient__ingredient__is_protein_source=True
        ).distinct()
    
    categories = Category.objects.all()
    
    context = {
        'recipes': recipes,
        'categories': categories,
        'meal_types': Recipe.MEAL_TYPE_CHOICES,
        'difficulties': Recipe.DIFFICULTY_CHOICES,
    }
    return render(request, 'recipes/recipe_list.html', context)

def recipe_detail(request, pk):
    """Show recipe details"""
    recipe = get_object_or_404(Recipe, pk=pk)
    ingredients = recipe.recipeingredient_set.all()
    
    
    ingredient_alternatives = {}
    for ri in ingredients:
        if ri.ingredient.is_protein_source:
            alternatives = ri.ingredient.alternatives.filter(is_protein_source=True)
            if alternatives:
                ingredient_alternatives[ri.ingredient.id] = alternatives
    
    context = {
        'recipe': recipe,
        'ingredients': ingredients,
        'nutrition': recipe.total_nutrition,
        'ingredient_alternatives': ingredient_alternatives,
    }
    return render(request, 'recipes/recipe_detail.html', context)

@csrf_exempt
def search_recipes(request):
    """AJAX search for recipes"""
    query = request.GET.get('q', '')
    meal_type = request.GET.get('meal_type', '')
    
    recipes = Recipe.objects.all()
    
    if query:
        recipes = recipes.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(tags__icontains=query)
        )
    
    if meal_type:
        recipes = recipes.filter(meal_type=meal_type)
    
    results = [{
        'id': r.id,
        'name': r.name,
        'meal_type': r.get_meal_type_display(),
        'prep_time': r.prep_time,
        'cook_time': r.cook_time,
        'image': r.image or '',
        'protein': r.total_nutrition['protein'],
    } for r in recipes[:10]]
    
    return JsonResponse({'recipes': results})

def get_protein_alternatives(request, ingredient_id):
    """Get protein alternatives for an ingredient"""
    ingredient = get_object_or_404(Ingredient, pk=ingredient_id)
    
    alternatives = []
    for alt in ingredient.alternatives.filter(is_protein_source=True):
        alternatives.append({
            'id': alt.id,
            'name': alt.name,
            'protein_per_100g': alt.protein,
            'calories_per_100g': alt.calories,
            'conversion_ratio': alt.protein / ingredient.protein if ingredient.protein > 0 else 1,
        })
    
    return JsonResponse({
        'original': {
            'id': ingredient.id,
            'name': ingredient.name,
            'protein_per_100g': ingredient.protein,
        },
        'alternatives': alternatives
    })

def protein_sources(request):
    """List all protein sources with alternatives"""
    protein_sources = Ingredient.objects.filter(is_protein_source=True).order_by('-protein')
    
    context = {
        'protein_sources': protein_sources,
    }
    return render(request, 'recipes/protein_sources.html', context)
