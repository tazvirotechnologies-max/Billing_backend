from rest_framework import serializers


class BillItemInputSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)


class BillCreateSerializer(serializers.Serializer):
    items = BillItemInputSerializer(many=True)
    payment_method = serializers.ChoiceField(choices=['CASH', 'UPI'])