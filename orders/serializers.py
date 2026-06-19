from rest_framework import serializers
from .models import Order, OrderItem
from rest_framework import serializers


#Order Item Serializer
class OrderItemSerializer(serializers.ModelSerializer):

    product_title = serializers.CharField(
        source="product.title",
        read_only=True
    )

    class Meta:
        model = OrderItem
        fields = [
            "id",
            "product",
            "product_title",
            "quantity_requested",
        ]


#Order response serializer
class OrderSerializer(serializers.ModelSerializer):

    items = OrderItemSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = Order
        fields = [
            "id",
            "store",
            "status",
            "created_at",
            "items",
        ]


#Create order item request serializer - POST /orders/
class CreateOrderItemSerializer(
    serializers.Serializer
):
    product_id = serializers.IntegerField()

    quantity_requested = serializers.IntegerField(
        min_value=1
    )

#Create order serializer - POST /orders/
class CreateOrderSerializer(
    serializers.Serializer
):
    store_id = serializers.IntegerField()

    items = CreateOrderItemSerializer(
        many=True,
        allow_empty=False
    )

class StoreOrderListSerializer(serializers.ModelSerializer):

    total_items = serializers.IntegerField(
        read_only=True
    )

    class Meta:
        model = Order
        fields = [
            "id",
            "status",
            "created_at",
            "total_items",
        ]