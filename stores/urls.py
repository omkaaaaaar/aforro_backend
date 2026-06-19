from django.urls import path

from .views import StoreInventoryAPIView

urlpatterns = [
    path(
        "<int:store_id>/inventory/",
        StoreInventoryAPIView.as_view(),
        name="store-inventory",
    ),
]