from django.db import models
from django.contrib.auth.models import User
from recipes.models import Recipe

class MealPlan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} ({self.start_date} to {self.end_date})"
    
    @property
    def total_days(self):
        return (self.end_date - self.start_date).days + 1
    
    @property
    def total_nutrition(self):
        """Calculate total nutrition for this meal plan"""
        nutrition = {'calories': 0, 'protein': 0, 'carbs': 0, 'fats': 0, 'fiber': 0}
        for meal in self.dailymeal_set.all():
            meal_nutrition = meal.nutrition
            for key in nutrition:
                nutrition[key] += meal_nutrition.get(key, 0)
        return nutrition

class DailyMeal(models.Model):
    MEAL_SLOT_CHOICES = [
        ('breakfast', 'Breakfast'),
        ('lunch', 'Lunch'),
        ('dinner', 'Dinner'),
        ('snack', 'Snack'),
        ('pre_workout', 'Pre-Workout'),
        ('post_workout', 'Post-Workout'),
    ]
    
    meal_plan = models.ForeignKey(MealPlan, on_delete=models.CASCADE)
    date = models.DateField()
    meal_slot = models.CharField(max_length=20, choices=MEAL_SLOT_CHOICES)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    servings = models.IntegerField(default=1)
    notes = models.TextField(blank=True)
    
    class Meta:
        ordering = ['date', 'meal_slot']
    
    def __str__(self):
        return f"{self.meal_slot} on {self.date}: {self.recipe.name}"
    
    @property
    def nutrition(self):
        """Calculate nutrition for this meal based on servings"""
        base_nutrition = self.recipe.total_nutrition
        factor = self.servings / self.recipe.servings
        return {k: v * factor for k, v in base_nutrition.items()}
