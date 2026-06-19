from rest_framework import serializers

from products.models import Product


class ProductSearchSerializer(
    serializers.ModelSerializer
):

    category_name = serializers.CharField(
        source="category.name",
        read_only=True
    )

    inventory_quantity = serializers.IntegerField(
        read_only=True,
        required=False,
        allow_null=True
    )

    class Meta:
        model = Product

        fields = [
            "id",
            "title",
            "description",
            "price",
            "category_name",
            "inventory_quantity",
            "created_at",
        ]