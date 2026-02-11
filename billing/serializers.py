from rest_framework import serializers

from .models import Bill, BillItem


# =========================
# INPUT (CREATE BILL)
# =========================
class BillItemInputSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)


class BillCreateSerializer(serializers.Serializer):
    items = BillItemInputSerializer(many=True)
    payment_method = serializers.ChoiceField(choices=["CASH", "UPI"])


# =========================
# OUTPUT (BILL HISTORY)
# =========================
class BillItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="product.name")

    class Meta:
        model = BillItem
        fields = [
            "product_name",
            "quantity",
            "price",
        ]


class BillListSerializer(serializers.ModelSerializer):
    cashier_name = serializers.CharField(source="cashier.username")

    class Meta:
        model = Bill
        fields = [
            "id",
            "bill_number",
            "created_at",
            "total_amount",
            "payment_method",
            "cashier_name",
        ]


class BillDetailSerializer(serializers.ModelSerializer):
    items = BillItemSerializer(many=True, read_only=True)
    cashier_name = serializers.CharField(source="cashier.username")

    class Meta:
        model = Bill
        fields = [
            "bill_number",
            "created_at",
            "payment_method",
            "total_amount",
            "cashier_name",
            "items",
        ]
