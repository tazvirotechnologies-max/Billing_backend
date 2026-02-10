from django.urls import path
from .views import (
    ProductListCreateView,
    ProductDetailView,
    CategoryListCreateView
)

urlpatterns = [
    path('products/', ProductListCreateView.as_view()),
    path('products/<int:pk>/', ProductDetailView.as_view()),
    path('categories/', CategoryListCreateView.as_view()),
]