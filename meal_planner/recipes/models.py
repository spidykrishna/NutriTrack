from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    
    class Meta:
        verbose_name_plural = "Categories"
    
    def __str__(self):
        return self.name

class Ingredient(models.Model):
    UNIT_CHOICES = [
        ('g', 'Grams'),
        ('kg', 'Kilograms'),
        ('ml', 'Milliliters'),
        ('l', 'Liters'),
        ('cup', 'Cups'),
        ('tbsp', 'Tablespoons'),
        ('tsp', 'Teaspoons'),
        ('piece', 'Pieces'),
        ('oz', 'Ounces'),
        ('lb', 'Pounds'),
    ]
    
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=100, blank=True)
    default_unit = models.CharField(max_length=20, choices=UNIT_CHOICES, default='g')
    
    # Nutritional info per 100g
    calories = models.FloatField(default=0)
    protein = models.FloatField(default=0)
    carbs = models.FloatField(default=0)
    fats = models.FloatField(default=0)
    fiber = models.FloatField(default=0)
    
    # Protein source flag
    is_protein_source = models.BooleanField(default=False)
    protein_quality_score = models.FloatField(default=0, help_text="PDCAAS or similar protein quality score")
    
    # Alternative ingredients
    alternatives = models.ManyToManyField('self', blank=True, symmetrical=False, related_name='alternative_to')
    
    def __str__(self):
        return self.name

class Recipe(models.Model):
    MEAL_TYPE_CHOICES = [
        ('breakfast', 'Breakfast'),
        ('lunch', 'Lunch'),
        ('dinner', 'Dinner'),
        ('snack', 'Snack'),
        ('pre_workout', 'Pre-Workout'),
        ('post_workout', 'Post-Workout'),
    ]
    
    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]
    
    name = models.CharField(max_length=200)
    description = models.TextField()
    meal_type = models.CharField(max_length=20, choices=MEAL_TYPE_CHOICES)
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default='easy')
    prep_time = models.IntegerField(help_text="Preparation time in minutes")
    cook_time = models.IntegerField(help_text="Cooking time in minutes")
    servings = models.IntegerField(default=1)
    image = models.URLField(blank=True, null=True)
    categories = models.ManyToManyField(Category, blank=True)
    
    # Instructions as JSON
    instructions = models.JSONField(default=list)
    
    # Tags for search
    tags = models.CharField(max_length=500, blank=True, help_text="Comma-separated tags")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    @property
    def total_time(self):
        return self.prep_time + self.cook_time
    
    @property
    def total_nutrition(self):
        """Calculate total nutrition based on ingredients"""
        nutrition = {'calories': 0, 'protein': 0, 'carbs': 0, 'fats': 0, 'fiber': 0}
        for ri in self.recipeingredient_set.all():
            factor = ri.amount / 100  # Nutrition values are per 100g
            nutrition['calories'] += ri.ingredient.calories * factor
            nutrition['protein'] += ri.ingredient.protein * factor
            nutrition['carbs'] += ri.ingredient.carbs * factor
            nutrition['fats'] += ri.ingredient.fats * factor
            nutrition['fiber'] += ri.ingredient.fiber * factor
        return nutrition

class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    amount = models.FloatField(help_text="Amount in the ingredient's default unit")
    unit = models.CharField(max_length=20, default='g')
    notes = models.CharField(max_length=200, blank=True)
    
    def __str__(self):
        return f"{self.amount}{self.unit} {self.ingredient.name} for {self.recipe.name}"

class ProteinAlternative(models.Model):
    """Model to store protein alternative mappings"""
    original = models.ForeignKey(Ingredient, on_delete=models.CASCADE, related_name='original_protein')
    alternative = models.ForeignKey(Ingredient, on_delete=models.CASCADE, related_name='alternative_protein')
    conversion_ratio = models.FloatField(default=1.0, help_text="Ratio to convert amounts")
    notes = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.original.name} -> {self.alternative.name}"
