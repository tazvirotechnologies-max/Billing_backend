from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.db.models import F
from .models import Ingredient, Recipe
from .serializers import IngredientSerializer, RecipeSerializer
from products.models import Product


class IngredientListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Admin only
        if request.user.role != 'ADMIN':
            return Response(status=status.HTTP_403_FORBIDDEN)

        ingredients = Ingredient.objects.all()
        return Response(IngredientSerializer(ingredients, many=True).data)

    def post(self, request):
        if request.user.role != 'ADMIN':
            return Response(status=status.HTTP_403_FORBIDDEN)

        serializer = IngredientSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=201)


class IngredientDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        if request.user.role != 'ADMIN':
            return Response(status=status.HTTP_403_FORBIDDEN)

        ingredient = Ingredient.objects.get(pk=pk)
        serializer = IngredientSerializer(
            ingredient,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    

class RecipeListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, product_id):
        # Admin only
        if request.user.role != 'ADMIN':
            return Response(status=status.HTTP_403_FORBIDDEN)

        recipes = Recipe.objects.filter(product_id=product_id)
        serializer = RecipeSerializer(recipes, many=True)
        return Response(serializer.data)

    def post(self, request, product_id):
        if request.user.role != 'ADMIN':
            return Response(status=status.HTTP_403_FORBIDDEN)

        data = request.data.copy()
        data['product'] = product_id

        serializer = RecipeSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=201)
    
class LowStockAlertView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role != 'ADMIN':
            return Response(status=status.HTTP_403_FORBIDDEN)

        low_stock_items = Ingredient.objects.filter(
            current_stock__lte=F('minimum_stock')
        )

        serializer = IngredientSerializer(low_stock_items, many=True)
        return Response(serializer.data)
    
class UnavailableProductsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):

        unavailable_products = set()

        # Loop through all recipes
        recipes = Recipe.objects.select_related(
            "product",
            "ingredient"
        )

        for recipe in recipes:

            ingredient = recipe.ingredient
            required_qty = recipe.quantity_used

            # If ingredient stock is insufficient
            if ingredient.current_stock < required_qty:
                unavailable_products.add(
                    recipe.product.id
                )

        return Response(list(unavailable_products))
