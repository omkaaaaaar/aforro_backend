from django.urls import reverse
from rest_framework.test import APITestCase

from products.models import Category, Product
from stores.models import Store, Inventory
from orders.models import Order


class OrderAPITest(APITestCase):

    def setUp(self):

        self.category = Category.objects.create(
            name="Electronics"
        )

        self.product = Product.objects.create(
            title="iPhone",
            price=50000,
            category=self.category,
        )

        self.store = Store.objects.create(
            name="Mumbai Store",
            location="Mumbai",
        )

        Inventory.objects.create(
            store=self.store,
            product=self.product,
            quantity=10,
        )

    def test_order_confirmed(self):

        payload = {
            "store_id": self.store.id,
            "items": [
                {
                    "product_id": self.product.id,
                    "quantity_requested": 2,
                }
            ],
        }

        response = self.client.post(
            "/orders/",
            payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            201,
        )

        order = Order.objects.first()

        self.assertEqual(
            order.status,
            Order.Status.CONFIRMED,
        )

    def test_order_rejected(self):

        payload = {
            "store_id": self.store.id,
            "items": [
                {
                    "product_id": self.product.id,
                    "quantity_requested": 999,
                }
            ],
        }

        response = self.client.post(
            "/orders/",
            payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            201,
        )

        order = Order.objects.first()

        self.assertEqual(
            order.status,
            Order.Status.REJECTED,
        )