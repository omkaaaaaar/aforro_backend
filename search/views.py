from django.db.models import Q, F

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from drf_spectacular.utils import (
    extend_schema,
    OpenApiParameter,
)

from products.models import Product

from .serializers import ProductSearchSerializer

from django.db.models import Case, When, IntegerField

from .throttles import (
    SuggestRateThrottle
)


@extend_schema(
    summary="Search Products",
    description="Search products by title, description, or category.",
    parameters=[
        OpenApiParameter(
            name="q",
            type=str,
            description="Search keyword",
            required=False,
        ),
        OpenApiParameter(
            name="category",
            type=int,
            description="Category ID",
            required=False,
        ),
        OpenApiParameter(
            name="min_price",
            type=float,
            description="Minimum price",
            required=False,
        ),
        OpenApiParameter(
            name="max_price",
            type=float,
            description="Maximum price",
            required=False,
        ),
        OpenApiParameter(
            name="store_id",
            type=int,
            description="Store ID",
            required=False,
        ),
        OpenApiParameter(
            name="in_stock",
            type=bool,
            description="Only products in stock",
            required=False,
        ),
        OpenApiParameter(
            name="sort",
            type=str,
            description="price, -price, newest",
            required=False,
        ),
    ],
    responses=ProductSearchSerializer(many=True),
)
class ProductSearchAPIView(APIView):

    def get(self, request):

        query = request.GET.get("q")

        category = request.GET.get("category")

        min_price = request.GET.get("min_price")

        max_price = request.GET.get("max_price")

        store_id = request.GET.get("store_id")

        in_stock = request.GET.get("in_stock")

        sort = request.GET.get("sort")

        products = Product.objects.select_related(
            "category"
        )

        # Keyword search
        if query:
            products = products.filter(
                Q(title__icontains=query)
                |
                Q(description__icontains=query)
                |
                Q(category__name__icontains=query)
            )

        # Category filter
        if category:
            products = products.filter(
                category_id=category
            )

        # Price filters
        if min_price:
            products = products.filter(
                price__gte=min_price
            )

        if max_price:
            products = products.filter(
                price__lte=max_price
            )

        # Store inventory quantity
        if store_id:
            products = products.annotate(
                inventory_quantity=F(
                    "inventory_records__quantity"
                )
            ).filter(
                inventory_records__store_id=store_id
            )

        # In stock filter
        if in_stock and in_stock.lower() == "true":
            products = products.filter(
                inventory_records__quantity__gt=0
            )

        # Sorting
        if sort == "price":
            products = products.order_by("price")

        elif sort == "-price":
            products = products.order_by("-price")

        elif sort == "newest":
            products = products.order_by("-created_at")

        # Prevent duplicate rows after joins
        products = products.distinct()

        # Pagination
        paginator = PageNumberPagination()

        paginated_products = paginator.paginate_queryset(
            products,
            request
        )

        serializer = ProductSearchSerializer(
            paginated_products,
            many=True
        )

        return paginator.get_paginated_response(
            serializer.data
        )


@extend_schema(
    summary="Product Suggestions",
    description=(
        "Autocomplete suggestions. "
        "Rate limited to 20 requests per minute."
    ),
    parameters=[
        OpenApiParameter(
            name="q",
            type=str,
            description="Minimum 3 characters"
        )
    ]
)

class ProductSuggestAPIView(APIView):

    throttle_classes = [
        SuggestRateThrottle
    ]

    def get(self, request):

        query = request.GET.get(
            "q",
            ""
        ).strip()

        if len(query) < 3:

            return Response(
                {
                    "error":
                    "Minimum 3 characters required"
                },
                status=400
            )

        suggestions = (
            Product.objects
            .filter(
                title__icontains=query
            )
            .annotate(
                priority=Case(
                    When(
                        title__istartswith=query,
                        then=0
                    ),
                    default=1,
                    output_field=IntegerField()
                )
            )
            .order_by(
                "priority",
                "title"
            )
            .values_list(
                "title",
                flat=True
            )[:10]
        )

        return Response(
            list(suggestions)
        )