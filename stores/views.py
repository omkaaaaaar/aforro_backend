from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Inventory
from .serializers import InventorySerializer
from drf_spectacular.utils import extend_schema


@extend_schema(
    summary="Store Inventory",
    description="Returns inventory for a store sorted alphabetically by product title.",
    responses=InventorySerializer(many=True),
)

class StoreInventoryAPIView(APIView):

    def get(self, request, store_id):

        inventory = (
            Inventory.objects
            .filter(store_id=store_id)
            .select_related(
                "product",
                "product__category"
            )
            .order_by("product__title")
        )

        serializer = InventorySerializer(
            inventory,
            many=True
        )

        return Response(serializer.data)