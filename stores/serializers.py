from rest_framework import serializers
from .models import Store

from .models import Inventory

#store
class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = [
            "id",
            "name",
            "location",
        ]

#inventory
class InventorySerializer(serializers.ModelSerializer):

    product_title = serializers.CharField(
        source="product.title",
        read_only=True
    )

    product_price = serializers.DecimalField(
        source="product.price",
        max_digits=10,
        decimal_places=2,
        read_only=True
    )

    category_name = serializers.CharField(
        source="product.category.name",
        read_only=True
    )

    class Meta:
        model = Inventory
        fields = [
            "id",
            "product_title",
            "product_price",
            "category_name",
            "quantity",
        ]