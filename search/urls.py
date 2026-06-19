from django.urls import path

from .views import (
    ProductSearchAPIView
)

urlpatterns = [

    path(
        "products/",
        ProductSearchAPIView.as_view(),
        name="product-search",
    ),

]