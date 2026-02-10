from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer


class ProductListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Cashier + Admin both can view
        products = Product.objects.filter(is_available=True)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    def post(self, request):
        # Admin only
        if request.user.role != 'ADMIN':
            return Response(status=status.HTTP_403_FORBIDDEN)

        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=201)


class ProductDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        if request.user.role != 'ADMIN':
            return Response(status=status.HTTP_403_FORBIDDEN)

        product = Product.objects.get(pk=pk)
        serializer = ProductSerializer(product, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class CategoryListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        categories = Category.objects.all()
        return Response(CategorySerializer(categories, many=True).data)

    def post(self, request):
        if request.user.role != 'ADMIN':
            return Response(status=status.HTTP_403_FORBIDDEN)

        serializer = CategorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=201)