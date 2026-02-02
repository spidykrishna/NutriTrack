from django.contrib import admin
from .models import Category, Ingredient, Recipe, RecipeIngredient, ProteinAlternative

class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'is_protein_source', 'protein', 'calories']
    list_filter = ['is_protein_source', 'category']
    search_fields = ['name']
    filter_horizontal = ['alternatives']

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ['name', 'meal_type', 'difficulty', 'prep_time', 'cook_time', 'servings']
    list_filter = ['meal_type', 'difficulty', 'categories']
    search_fields = ['name', 'description', 'tags']
    filter_horizontal = ['categories']
    inlines = [RecipeIngredientInline]

@admin.register(ProteinAlternative)
class ProteinAlternativeAdmin(admin.ModelAdmin):
    list_display = ['original', 'alternative', 'conversion_ratio']
    list_filter = ['original__category']
