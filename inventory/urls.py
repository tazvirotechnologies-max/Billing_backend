from django.urls import path
from .views import (
    IngredientListCreateView,
    IngredientDetailView,
    RecipeListCreateView
)

urlpatterns = [
    path('ingredients/', IngredientListCreateView.as_view()),
    path('ingredients/<int:pk>/', IngredientDetailView.as_view()),

    # Recipe mapping
    path('products/<int:product_id>/recipes/', RecipeListCreateView.as_view()),
]