from django.db import models
from django.contrib.auth.models import User
from meal_plans.models import MealPlan
from recipes.models import Ingredient

class ShoppingList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    meal_plan = models.OneToOneField(MealPlan, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, default="Shopping List")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} - {self.created_at.strftime('%Y-%m-%d')}"
    
    def generate_from_meal_plan(self):
        """Generate shopping list items from meal plan"""
        if not self.meal_plan:
            return
        
        # Clear existing items
        self.items.all().delete()
        
        # Aggregate ingredients from all meals
        ingredient_totals = {}
        
        for daily_meal in self.meal_plan.dailymeal_set.all():
            recipe = daily_meal.recipe
            servings_factor = daily_meal.servings / recipe.servings
            
            for ri in recipe.recipeingredient_set.all():
                ingredient = ri.ingredient
                amount = ri.amount * servings_factor
                
                if ingredient.id in ingredient_totals:
                    ingredient_totals[ingredient.id]['amount'] += amount
                else:
                    ingredient_totals[ingredient.id] = {
                        'ingredient': ingredient,
                        'amount': amount,
                        'unit': ri.unit
                    }
        
        # Create shopping list items
        for data in ingredient_totals.values():
            ShoppingListItem.objects.create(
                shopping_list=self,
                ingredient=data['ingredient'],
                amount=round(data['amount'], 2),
                unit=data['unit']
            )

class ShoppingListItem(models.Model):
    shopping_list = models.ForeignKey(ShoppingList, on_delete=models.CASCADE, related_name='items')
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    amount = models.FloatField()
    unit = models.CharField(max_length=20)
    purchased = models.BooleanField(default=False)
    notes = models.CharField(max_length=200, blank=True)
    
    class Meta:
        ordering = ['purchased', 'ingredient__name']
    
    def __str__(self):
        status = "✓" if self.purchased else "○"
        return f"{status} {self.amount} {self.unit} {self.ingredient.name}"
