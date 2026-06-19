from django.db import transaction
from django.db.models import F

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from stores.models import Store, Inventory

from .models import Order, OrderItem
from .serializers import (
    CreateOrderSerializer,
    OrderSerializer,
    StoreOrderListSerializer,
)
from drf_spectacular.utils import extend_schema

from django.db.models import Count


@extend_schema(
    request=CreateOrderSerializer,
    responses=OrderSerializer,
    summary="Create Order",
    description="Create an order and deduct inventory if stock is available."
)

class CreateOrderAPIView(APIView):

    @transaction.atomic
    def post(self, request):

        serializer = CreateOrderSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        data = serializer.validated_data

        try:
            store = Store.objects.get(
                id=data["store_id"]
            )

        except Store.DoesNotExist:
            return Response(
                {"error": "Store not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        inventory_records = []
        all_available = True

        for item in data["items"]:

            product_id = item["product_id"]
            quantity_requested = item["quantity_requested"]

            try:

                inventory = (
                    Inventory.objects
                    .select_for_update()
                    .get(
                        store=store,
                        product_id=product_id,
                    )
                )

            except Inventory.DoesNotExist:
                all_available = False
                break

            if inventory.quantity < quantity_requested:
                all_available = False
                break

            inventory_records.append(
                (
                    inventory,
                    quantity_requested,
                )
            )

        if not all_available:

            order = Order.objects.create(
                store=store,
                status=Order.Status.REJECTED,
            )

            for item in data["items"]:

                OrderItem.objects.create(
                    order=order,
                    product_id=item["product_id"],
                    quantity_requested=item[
                        "quantity_requested"
                    ],
                )

            return Response(
                OrderSerializer(order).data,
                status=status.HTTP_201_CREATED,
            )

        order = Order.objects.create(
            store=store,
            status=Order.Status.CONFIRMED,
        )

        for item in data["items"]:

            OrderItem.objects.create(
                order=order,
                product_id=item["product_id"],
                quantity_requested=item[
                    "quantity_requested"
                ],
            )

        for inventory, quantity in inventory_records:

            Inventory.objects.filter(
                id=inventory.id
            ).update(
                quantity=F("quantity") - quantity
            )

        return Response(
            OrderSerializer(order).data,
            status=status.HTTP_201_CREATED,
        )


class StoreOrdersAPIView(APIView):

    def get(self, request, store_id):

        orders = (
            Order.objects
            .filter(store_id=store_id)
            .annotate(
                total_items=Count("items")
            )
            .order_by("-created_at")
        )

        serializer = StoreOrderListSerializer(
            orders,
            many=True
        )

        return Response(serializer.data)