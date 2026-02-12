from django.urls import path
from .views import (
    IngredientListCreateView,
    IngredientDetailView,
    RecipeListCreateView,
    LowStockAlertView,
    UnavailableProductsView
)

urlpatterns = [
    path('ingredients/', IngredientListCreateView.as_view()),
    path('ingredients/<int:pk>/', IngredientDetailView.as_view()),

    # Recipe mapping
    path('products/<int:product_id>/recipes/', RecipeListCreateView.as_view()),

    # 🔔 Low stock alerts
    path('inventory/low-stock/', LowStockAlertView.as_view()),

    path(
    'unavailable-products/',
    UnavailableProductsView.as_view()
),

]