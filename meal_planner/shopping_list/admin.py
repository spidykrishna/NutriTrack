from django.contrib import admin
from .models import ShoppingList, ShoppingListItem

class ShoppingListItemInline(admin.TabularInline):
    model = ShoppingListItem
    extra = 0

@admin.register(ShoppingList)
class ShoppingListAdmin(admin.ModelAdmin):
    list_display = ['name', 'meal_plan', 'created_at', 'item_count']
    list_filter = ['created_at']
    search_fields = ['name']
    inlines = [ShoppingListItemInline]
    
    def item_count(self, obj):
        return obj.items.count()
    item_count.short_description = 'Items'

@admin.register(ShoppingListItem)
class ShoppingListItemAdmin(admin.ModelAdmin):
    list_display = ['ingredient', 'amount', 'unit', 'purchased', 'shopping_list']
    list_filter = ['purchased']
    search_fields = ['ingredient__name']
