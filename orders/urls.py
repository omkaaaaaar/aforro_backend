from django.urls import path

from .views import (
    CreateOrderAPIView,
    StoreOrdersAPIView,
)

urlpatterns = [
    path(
        "",
        CreateOrderAPIView.as_view(),
        name="create-order",
    ),

    path(
        "stores/<int:store_id>/orders/",
        StoreOrdersAPIView.as_view(),
        name="store-orders",
    ),
]