#!/usr/bin/env python
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'meal_planner.settings')
sys.path.insert(0, '/mnt/okcomputer/output/meal_planner')
django.setup()

from recipes.models import Category, Ingredient, Recipe, RecipeIngredient
from meal_plans.models import MealPlan, DailyMeal
from nutrients.models import NutritionGoal
from datetime import datetime, timedelta

def create_categories():
    categories = [
        "High Protein",
        "Low Carb",
        "Vegetarian",
        "Vegan",
        "Quick Meals",
        "Post-Workout",
        "Pre-Workout",
    ]
    for name in categories:
        Category.objects.get_or_create(name=name)
    print(f"Created {len(categories)} categories")

def create_ingredients():
    ingredients_data = [
        # Protein Sources
        {"name": "Chicken Breast", "category": "Meat", "is_protein_source": True, "protein": 31, "calories": 165, "carbs": 0, "fats": 3.6, "fiber": 0},
        {"name": "Salmon", "category": "Fish", "is_protein_source": True, "protein": 25, "calories": 208, "carbs": 0, "fats": 13, "fiber": 0},
        {"name": "Eggs", "category": "Dairy", "is_protein_source": True, "protein": 13, "calories": 155, "carbs": 1.1, "fats": 11, "fiber": 0},
        {"name": "Greek Yogurt", "category": "Dairy", "is_protein_source": True, "protein": 10, "calories": 59, "carbs": 3.6, "fats": 0.4, "fiber": 0},
        {"name": "Whey Protein", "category": "Supplements", "is_protein_source": True, "protein": 80, "calories": 400, "carbs": 8, "fats": 8, "fiber": 0},
        {"name": "Tofu", "category": "Vegan", "is_protein_source": True, "protein": 8, "calories": 76, "carbs": 1.9, "fats": 4.8, "fiber": 0.3},
        {"name": "Tempeh", "category": "Vegan", "is_protein_source": True, "protein": 19, "calories": 193, "carbs": 9, "fats": 11, "fiber": 0},
        {"name": "Lentils", "category": "Legumes", "is_protein_source": True, "protein": 9, "calories": 116, "carbs": 20, "fats": 0.4, "fiber": 8},
        {"name": "Chickpeas", "category": "Legumes", "is_protein_source": True, "protein": 19, "calories": 364, "carbs": 61, "fats": 6, "fiber": 17},
        {"name": "Quinoa", "category": "Grains", "is_protein_source": True, "protein": 4.4, "calories": 120, "carbs": 21, "fats": 1.9, "fiber": 2.8},
        {"name": "Cottage Cheese", "category": "Dairy", "is_protein_source": True, "protein": 11, "calories": 98, "carbs": 3.4, "fats": 4.3, "fiber": 0},
        {"name": "Turkey Breast", "category": "Meat", "is_protein_source": True, "protein": 29, "calories": 135, "carbs": 0, "fats": 1, "fiber": 0},
        {"name": "Tuna", "category": "Fish", "is_protein_source": True, "protein": 30, "calories": 132, "carbs": 0, "fats": 1, "fiber": 0},
        {"name": "Edamame", "category": "Vegan", "is_protein_source": True, "protein": 11, "calories": 122, "carbs": 10, "fats": 5, "fiber": 5},
        {"name": "Paneer", "category": "Dairy", "is_protein_source": True, "protein": 18, "calories": 265, "carbs": 6, "fats": 20, "fiber": 0},
        
        # Other ingredients
        {"name": "Brown Rice", "category": "Grains", "protein": 2.6, "calories": 111, "carbs": 23, "fats": 0.9, "fiber": 1.8},
        {"name": "Oats", "category": "Grains", "protein": 16.9, "calories": 389, "carbs": 66, "fats": 6.9, "fiber": 10.6},
        {"name": "Sweet Potato", "category": "Vegetables", "protein": 1.6, "calories": 86, "carbs": 20, "fats": 0.1, "fiber": 3},
        {"name": "Broccoli", "category": "Vegetables", "protein": 2.8, "calories": 34, "carbs": 7, "fats": 0.4, "fiber": 2.6},
        {"name": "Spinach", "category": "Vegetables", "protein": 2.9, "calories": 23, "carbs": 3.6, "fats": 0.4, "fiber": 2.2},
        {"name": "Avocado", "category": "Fruits", "protein": 2, "calories": 160, "carbs": 8.5, "fats": 15, "fiber": 6.7},
        {"name": "Banana", "category": "Fruits", "protein": 1.1, "calories": 89, "carbs": 23, "fats": 0.3, "fiber": 2.6},
        {"name": "Almonds", "category": "Nuts", "protein": 21, "calories": 579, "carbs": 22, "fats": 49, "fiber": 12.5},
        {"name": "Olive Oil", "category": "Oils", "protein": 0, "calories": 884, "carbs": 0, "fats": 100, "fiber": 0},
        {"name": "Garlic", "category": "Vegetables", "protein": 6.4, "calories": 149, "carbs": 33, "fats": 0.5, "fiber": 2.1},
        {"name": "Ginger", "category": "Vegetables", "protein": 1.8, "calories": 80, "carbs": 18, "fats": 0.8, "fiber": 2},
        {"name": "Turmeric", "category": "Spices", "protein": 7.8, "calories": 312, "carbs": 67, "fats": 3.3, "fiber": 22.7},
        {"name": "Cumin", "category": "Spices", "protein": 17.8, "calories": 375, "carbs": 44, "fats": 22, "fiber": 10.5},
        {"name": "Coriander", "category": "Spices", "protein": 12.4, "calories": 298, "carbs": 55, "fats": 17, "fiber": 41.9},
        {"name": "Tomato", "category": "Vegetables", "protein": 0.9, "calories": 18, "carbs": 3.9, "fats": 0.2, "fiber": 1.2},
        {"name": "Onion", "category": "Vegetables", "protein": 1.1, "calories": 40, "carbs": 9, "fats": 0.1, "fiber": 1.7},
        {"name": "Bell Pepper", "category": "Vegetables", "protein": 0.99, "calories": 31, "carbs": 6, "fats": 0.3, "fiber": 2.1},
        {"name": "Mushrooms", "category": "Vegetables", "protein": 3.1, "calories": 22, "carbs": 3.3, "fats": 0.3, "fiber": 1},
    ]
    
    created = []
    for data in ingredients_data:
        ing, _ = Ingredient.objects.get_or_create(name=data["name"], defaults=data)
        created.append(ing)
    
    print(f"Created {len(created)} ingredients")
    return created

def create_protein_alternatives():
    # Set up alternative relationships for protein sources
    alternatives_map = {
        "Chicken Breast": ["Turkey Breast", "Tofu", "Tempeh"],
        "Paneer": ["Tofu", "Tempeh", "Cottage Cheese"],
        "Lentils": ["Chickpeas", "Quinoa", "Edamame"],
        "Eggs": ["Greek Yogurt", "Cottage Cheese"],
        "Salmon": ["Tuna", "Chicken Breast"],
    }
    
    for orig_name, alt_names in alternatives_map.items():
        try:
            original = Ingredient.objects.get(name=orig_name)
            for alt_name in alt_names:
                try:
                    alt = Ingredient.objects.get(name=alt_name)
                    original.alternatives.add(alt)
                except Ingredient.DoesNotExist:
                    pass
        except Ingredient.DoesNotExist:
            pass
    
    print("Created protein alternative relationships")

def create_recipes():
    recipes_data = [
        {
            "name": "Grilled Chicken Breast with Quinoa",
            "description": "A high-protein, balanced meal perfect for post-workout recovery. Features tender grilled chicken breast served with fluffy quinoa and steamed vegetables.",
            "meal_type": "lunch",
            "difficulty": "easy",
            "prep_time": 10,
            "cook_time": 20,
            "servings": 2,
            "tags": "high-protein, healthy, post-workout, chicken",
            "instructions": [
                "Season chicken breast with salt, pepper, and your favorite herbs",
                "Grill chicken on medium-high heat for 6-7 minutes per side until internal temperature reaches 165°F",
                "Rinse quinoa and cook according to package instructions",
                "Steam broccoli and bell peppers for 5 minutes",
                "Plate chicken over quinoa with vegetables on the side"
            ],
            "ingredients": [
                ("Chicken Breast", 200, "g"),
                ("Quinoa", 100, "g"),
                ("Broccoli", 150, "g"),
                ("Bell Pepper", 100, "g"),
                ("Olive Oil", 15, "ml"),
                ("Garlic", 10, "g"),
            ]
        },
        {
            "name": "Protein-Packed Greek Yogurt Bowl",
            "description": "A delicious breakfast bowl loaded with protein from Greek yogurt, topped with fresh fruits and almonds for sustained energy.",
            "meal_type": "breakfast",
            "difficulty": "easy",
            "prep_time": 5,
            "cook_time": 0,
            "servings": 1,
            "tags": "breakfast, high-protein, vegetarian, quick",
            "instructions": [
                "Add Greek yogurt to a bowl",
                "Top with sliced banana and berries",
                "Sprinkle with almonds and a drizzle of honey",
                "Add a scoop of whey protein if desired"
            ],
            "ingredients": [
                ("Greek Yogurt", 200, "g"),
                ("Banana", 100, "g"),
                ("Almonds", 30, "g"),
                ("Whey Protein", 30, "g"),
            ]
        },
        {
            "name": "Salmon with Sweet Potato and Spinach",
            "description": "Omega-3 rich salmon paired with complex carbs from sweet potato and nutrient-dense spinach. Perfect for dinner.",
            "meal_type": "dinner",
            "difficulty": "medium",
            "prep_time": 15,
            "cook_time": 25,
            "servings": 2,
            "tags": "omega-3, high-protein, dinner, healthy-fats",
            "instructions": [
                "Preheat oven to 400°F",
                "Season salmon with lemon, dill, salt, and pepper",
                "Bake salmon for 12-15 minutes",
                "Roast cubed sweet potato with olive oil for 25 minutes",
                "Sauté spinach with garlic until wilted",
                "Serve salmon with sweet potato and spinach"
            ],
            "ingredients": [
                ("Salmon", 250, "g"),
                ("Sweet Potato", 300, "g"),
                ("Spinach", 150, "g"),
                ("Olive Oil", 20, "ml"),
                ("Garlic", 10, "g"),
            ]
        },
        {
            "name": "Tofu Stir-Fry with Brown Rice",
            "description": "A plant-based protein powerhouse featuring crispy tofu stir-fried with colorful vegetables over brown rice.",
            "meal_type": "dinner",
            "difficulty": "medium",
            "prep_time": 15,
            "cook_time": 20,
            "servings": 2,
            "tags": "vegan, high-protein, plant-based, asian",
            "instructions": [
                "Press tofu to remove excess water, then cube",
                "Pan-fry tofu until golden and crispy",
                "Stir-fry vegetables with ginger and garlic",
                "Add tofu back to the pan with soy sauce",
                "Serve over cooked brown rice"
            ],
            "ingredients": [
                ("Tofu", 300, "g"),
                ("Brown Rice", 150, "g"),
                ("Broccoli", 150, "g"),
                ("Bell Pepper", 100, "g"),
                ("Mushrooms", 100, "g"),
                ("Ginger", 10, "g"),
                ("Garlic", 10, "g"),
                ("Olive Oil", 15, "ml"),
            ]
        },
        {
            "name": "Egg White Omelette with Vegetables",
            "description": "A lean protein breakfast featuring fluffy egg whites loaded with fresh vegetables and herbs.",
            "meal_type": "breakfast",
            "difficulty": "easy",
            "prep_time": 5,
            "cook_time": 10,
            "servings": 1,
            "tags": "low-fat, high-protein, breakfast, quick",
            "instructions": [
                "Whisk egg whites with salt and pepper",
                "Sauté vegetables in a non-stick pan",
                "Pour egg whites over vegetables",
                "Cook until set, then fold and serve"
            ],
            "ingredients": [
                ("Eggs", 200, "g"),
                ("Spinach", 50, "g"),
                ("Tomato", 50, "g"),
                ("Mushrooms", 50, "g"),
                ("Olive Oil", 5, "ml"),
            ]
        },
        {
            "name": "Chickpea and Quinoa Salad",
            "description": "A refreshing, protein-rich salad perfect for lunch. Features chickpeas, quinoa, and fresh vegetables with a lemon dressing.",
            "meal_type": "lunch",
            "difficulty": "easy",
            "prep_time": 15,
            "cook_time": 15,
            "servings": 2,
            "tags": "vegan, high-protein, salad, meal-prep",
            "instructions": [
                "Cook quinoa according to package instructions and let cool",
                "Rinse and drain chickpeas",
                "Chop cucumber, tomato, and bell pepper",
                "Mix all ingredients in a large bowl",
                "Dress with lemon juice, olive oil, salt, and pepper"
            ],
            "ingredients": [
                ("Chickpeas", 200, "g"),
                ("Quinoa", 100, "g"),
                ("Cucumber", 100, "g"),
                ("Tomato", 100, "g"),
                ("Bell Pepper", 50, "g"),
                ("Olive Oil", 15, "ml"),
                ("Lemon", 1, "piece"),
            ]
        },
        {
            "name": "Pre-Workout Banana Oat Smoothie",
            "description": "Energy-boosting smoothie with complex carbs from oats and natural sugars from banana. Perfect 30-60 minutes before training.",
            "meal_type": "pre_workout",
            "difficulty": "easy",
            "prep_time": 5,
            "cook_time": 0,
            "servings": 1,
            "tags": "pre-workout, energy, smoothie, quick",
            "instructions": [
                "Blend oats into a fine powder",
                "Add banana, protein powder, and milk",
                "Blend until smooth",
                "Add ice if desired and blend again"
            ],
            "ingredients": [
                ("Oats", 50, "g"),
                ("Banana", 100, "g"),
                ("Whey Protein", 30, "g"),
                ("Almonds", 10, "g"),
            ]
        },
        {
            "name": "Post-Workout Protein Shake",
            "description": "Rapidly absorbed protein shake to support muscle recovery immediately after training.",
            "meal_type": "post_workout",
            "difficulty": "easy",
            "prep_time": 2,
            "cook_time": 0,
            "servings": 1,
            "tags": "post-workout, recovery, protein-shake, quick",
            "instructions": [
                "Add whey protein to shaker",
                "Add water or milk",
                "Shake vigorously for 30 seconds",
                "Consume within 30 minutes post-workout"
            ],
            "ingredients": [
                ("Whey Protein", 40, "g"),
                ("Banana", 50, "g"),
            ]
        },
        {
            "name": "Paneer Tikka with Brown Rice",
            "description": "Flavorful Indian-style grilled paneer with aromatic spices, served with brown rice.",
            "meal_type": "dinner",
            "difficulty": "medium",
            "prep_time": 20,
            "cook_time": 25,
            "servings": 2,
            "tags": "indian, high-protein, vegetarian, flavorful",
            "instructions": [
                "Marinate paneer cubes in yogurt and spices for 15 minutes",
                "Grill or pan-fry paneer until golden",
                "Sauté onions, tomatoes, and bell peppers",
                "Add paneer and simmer for 10 minutes",
                "Serve with brown rice"
            ],
            "ingredients": [
                ("Paneer", 250, "g"),
                ("Brown Rice", 150, "g"),
                ("Onion", 100, "g"),
                ("Tomato", 100, "g"),
                ("Bell Pepper", 100, "g"),
                ("Greek Yogurt", 50, "g"),
                ("Ginger", 10, "g"),
                ("Garlic", 10, "g"),
                ("Cumin", 5, "g"),
                ("Coriander", 5, "g"),
                ("Turmeric", 3, "g"),
                ("Olive Oil", 15, "ml"),
            ]
        },
        {
            "name": "Lentil Curry with Quinoa",
            "description": "Hearty and nutritious lentil curry packed with plant-based protein and fiber.",
            "meal_type": "lunch",
            "difficulty": "easy",
            "prep_time": 10,
            "cook_time": 30,
            "servings": 3,
            "tags": "vegan, high-protein, high-fiber, indian",
            "instructions": [
                "Rinse lentils and set aside",
                "Sauté onions, ginger, and garlic",
                "Add spices and toast for 1 minute",
                "Add lentils and water, simmer for 25 minutes",
                "Serve with cooked quinoa"
            ],
            "ingredients": [
                ("Lentils", 200, "g"),
                ("Quinoa", 150, "g"),
                ("Onion", 100, "g"),
                ("Tomato", 100, "g"),
                ("Ginger", 15, "g"),
                ("Garlic", 15, "g"),
                ("Cumin", 5, "g"),
                ("Coriander", 5, "g"),
                ("Turmeric", 3, "g"),
                ("Olive Oil", 15, "ml"),
            ]
        },
    ]
    
    for recipe_data in recipes_data:
        ingredients_data = recipe_data.pop("ingredients")
        recipe, created = Recipe.objects.get_or_create(
            name=recipe_data["name"],
            defaults=recipe_data
        )
        
        if created:
            # Add ingredients
            for ing_name, amount, unit in ingredients_data:
                try:
                    ingredient = Ingredient.objects.get(name=ing_name)
                    RecipeIngredient.objects.create(
                        recipe=recipe,
                        ingredient=ingredient,
                        amount=amount,
                        unit=unit
                    )
                except Ingredient.DoesNotExist:
                    print(f"Ingredient not found: {ing_name}")
    
    print(f"Created {len(recipes_data)} recipes")

def create_nutrition_goals():
    NutritionGoal.objects.get_or_create(
        user=None,
        defaults={
            "daily_calories": 2200,
            "daily_protein": 150,
            "daily_carbs": 250,
            "daily_fats": 70,
            "daily_fiber": 30,
            "protein_percentage": 30,
            "carbs_percentage": 45,
            "fats_percentage": 25,
        }
    )
    print("Created default nutrition goals")

def main():
    print("Creating sample data...")
    create_categories()
    create_ingredients()
    create_protein_alternatives()
    create_recipes()
    create_nutrition_goals()
    print("\nSample data created successfully!")

if __name__ == "__main__":
    main()
