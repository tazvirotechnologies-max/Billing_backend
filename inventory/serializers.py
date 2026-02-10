from rest_framework import serializers
from .models import Ingredient, Recipe
from products.models import Product


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'unit', 'current_stock', 'minimum_stock')


class RecipeSerializer(serializers.ModelSerializer):
    ingredient_name = serializers.ReadOnlyField(source='ingredient.name')
    ingredient_unit = serializers.ReadOnlyField(source='ingredient.unit')

    class Meta:
        model = Recipe
        fields = (
            'id',
            'product',
            'ingredient',
            'ingredient_name',
            'ingredient_unit',
            'quantity_used',
        )