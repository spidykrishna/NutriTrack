from django.urls import path
from . import views

urlpatterns = [
    path('shopping-lists/', views.shopping_lists, name='shopping_lists'),
    path('shopping-list/', views.shopping_list_detail, name='shopping_list_detail'),
    path('shopping-list/<int:pk>/', views.shopping_list_detail, name='shopping_list_detail'),
    path('meal-plans/<int:plan_id>/generate-shopping-list/', views.generate_shopping_list, name='generate_shopping_list'),
    path('shopping-items/<int:item_id>/toggle/', views.toggle_item_purchased, name='toggle_item_purchased'),
    path('shopping-items/<int:item_id>/update/', views.update_item_amount, name='update_item_amount'),
    path('shopping-items/<int:item_id>/remove/', views.remove_item, name='remove_item'),
    path('shopping-list/<int:list_id>/add-item/', views.add_custom_item, name='add_custom_item'),
    path('shopping-list/<int:list_id>/clear-purchased/', views.clear_purchased, name='clear_purchased'),
    
]
