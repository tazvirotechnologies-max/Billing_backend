from django.contrib import admin
from .models import Ingredient, Recipe


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'unit', 'current_stock', 'minimum_stock')


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('product', 'ingredient', 'quantity_used')
    list_filter = ('product',)