from django.db import models
from django.contrib.auth.models import User
from meal_plans.models import MealPlan

class NutritionGoal(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    daily_calories = models.FloatField(default=2000)
    daily_protein = models.FloatField(default=150, help_text="in grams")
    daily_carbs = models.FloatField(default=250, help_text="in grams")
    daily_fats = models.FloatField(default=70, help_text="in grams")
    daily_fiber = models.FloatField(default=30, help_text="in grams")
    
    # Macro split preferences
    protein_percentage = models.IntegerField(default=30)
    carbs_percentage = models.IntegerField(default=40)
    fats_percentage = models.IntegerField(default=30)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Nutrition Goals: {self.daily_calories} cal, {self.daily_protein}g protein"

class NutritionLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateField()
    meal_plan = models.ForeignKey(MealPlan, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Actual intake
    calories_consumed = models.FloatField(default=0)
    protein_consumed = models.FloatField(default=0)
    carbs_consumed = models.FloatField(default=0)
    fats_consumed = models.FloatField(default=0)
    fiber_consumed = models.FloatField(default=0)
    
    notes = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-date']
        unique_together = ['user', 'date']
    
    def __str__(self):
        return f"Nutrition Log - {self.date}"
    
    @property
    def protein_percentage(self):
        if self.calories_consumed == 0:
            return 0
        return (self.protein_consumed * 4 / self.calories_consumed) * 100
    
    @property
    def carbs_percentage(self):
        if self.calories_consumed == 0:
            return 0
        return (self.carbs_consumed * 4 / self.calories_consumed) * 100
    
    @property
    def fats_percentage(self):
        if self.calories_consumed == 0:
            return 0
        return (self.fats_consumed * 9 / self.calories_consumed) * 100
    
    def compare_with_goals(self, goals):
        """Compare actual intake with goals"""
        return {
            'calories': {
                'consumed': self.calories_consumed,
                'goal': goals.daily_calories,
                'remaining': goals.daily_calories - self.calories_consumed,
                'percentage': (self.calories_consumed / goals.daily_calories * 100) if goals.daily_calories > 0 else 0
            },
            'protein': {
                'consumed': self.protein_consumed,
                'goal': goals.daily_protein,
                'remaining': goals.daily_protein - self.protein_consumed,
                'percentage': (self.protein_consumed / goals.daily_protein * 100) if goals.daily_protein > 0 else 0
            },
            'carbs': {
                'consumed': self.carbs_consumed,
                'goal': goals.daily_carbs,
                'remaining': goals.daily_carbs - self.carbs_consumed,
                'percentage': (self.carbs_consumed / goals.daily_carbs * 100) if goals.daily_carbs > 0 else 0
            },
            'fats': {
                'consumed': self.fats_consumed,
                'goal': goals.daily_fats,
                'remaining': goals.daily_fats - self.fats_consumed,
                'percentage': (self.fats_consumed / goals.daily_fats * 100) if goals.daily_fats > 0 else 0
            },
            'fiber': {
                'consumed': self.fiber_consumed,
                'goal': goals.daily_fiber,
                'remaining': goals.daily_fiber - self.fiber_consumed,
                'percentage': (self.fiber_consumed / goals.daily_fiber * 100) if goals.daily_fiber > 0 else 0
            }
        }
