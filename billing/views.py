from datetime import datetime

from django.db import transaction
from django.utils.timezone import now

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.exceptions import PermissionDenied

from .models import Bill, BillItem
from .serializers import (
    BillCreateSerializer,
    BillListSerializer,
    BillDetailSerializer,
)
from products.models import Product
from inventory.models import Ingredient, Recipe


# =========================
# CREATE BILL (EXISTING)
# =========================
class CreateBillView(APIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request):
        serializer = BillCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        items = serializer.validated_data["items"]
        payment_method = serializer.validated_data["payment_method"]

        ingredient_usage = {}
        total_amount = 0

        # 1️⃣ COLLECT REQUIRED INGREDIENTS
        for item in items:
            product = Product.objects.get(id=item["product_id"])
            quantity = item["quantity"]

            total_amount += product.price * quantity

            recipes = Recipe.objects.filter(product=product)
            if not recipes.exists():
                return Response(
                    {"detail": f"No recipe defined for {product.name}"},
                    status=400,
                )

            for recipe in recipes:
                required_qty = recipe.quantity_used * quantity
                ingredient_id = recipe.ingredient_id

                ingredient_usage.setdefault(ingredient_id, 0)
                ingredient_usage[ingredient_id] += required_qty

        # 2️⃣ CHECK STOCK
        for ingredient_id, required_qty in ingredient_usage.items():
            ingredient = Ingredient.objects.select_for_update().get(
                id=ingredient_id
            )

            if ingredient.current_stock < required_qty:
                return Response(
                    {
                        "detail": f"Not enough stock for {ingredient.name}",
                        "required": required_qty,
                        "available": ingredient.current_stock,
                    },
                    status=400,
                )

        # 3️⃣ DEDUCT STOCK
        for ingredient_id, required_qty in ingredient_usage.items():
            ingredient = Ingredient.objects.get(id=ingredient_id)
            ingredient.current_stock -= required_qty
            ingredient.save()

        # 4️⃣ CREATE BILL
        bill_number = f"BILL-{now().strftime('%Y%m%d%H%M%S')}"

        bill = Bill.objects.create(
            bill_number=bill_number,
            cashier=request.user,
            payment_method=payment_method,
            total_amount=total_amount,
        )

        # 5️⃣ CREATE BILL ITEMS
        for item in items:
            product = Product.objects.get(id=item["product_id"])
            BillItem.objects.create(
                bill=bill,
                product=product,
                quantity=item["quantity"],
                price=product.price,
            )

        return Response(
            {
                "bill_number": bill.bill_number,
                "total_amount": bill.total_amount,
            },
            status=201,
        )


# =========================
# BILL HISTORY (LIST)
# =========================
class BillListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BillListSerializer

    def get_queryset(self):
        user = self.request.user
        qs = Bill.objects.select_related("cashier").order_by("-created_at")

        # 🔐 Role-based visibility
        if user.role != "ADMIN":
            qs = qs.filter(cashier=user)

        # 📅 Today filter
        if self.request.query_params.get("today"):
            today = datetime.today().date()
            qs = qs.filter(created_at__date=today)

        # 📆 Date range filter
        start = self.request.query_params.get("from")
        end = self.request.query_params.get("to")

        if start and end:
            qs = qs.filter(
                created_at__date__gte=start,
                created_at__date__lte=end,
            )

        return qs


# =========================
# BILL DETAIL
# =========================
class BillDetailView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BillDetailSerializer
    queryset = Bill.objects.prefetch_related("items__product")

    def get_object(self):
        bill = super().get_object()
        user = self.request.user

        # 🔐 Staff can only see own bills
        if user.role != "ADMIN" and bill.cashier != user:
            raise PermissionDenied("You are not allowed to view this bill")

        return bill
