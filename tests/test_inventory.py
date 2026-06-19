from rest_framework.test import APITestCase

from products.models import Category, Product
from stores.models import Store, Inventory


class InventoryAPITest(APITestCase):

    def setUp(self):

        category = Category.objects.create(
            name="Electronics"
        )

        product = Product.objects.create(
            title="iPhone",
            price=50000,
            category=category,
        )

        self.store = Store.objects.create(
            name="Store",
            location="Mumbai",
        )

        Inventory.objects.create(
            store=self.store,
            product=product,
            quantity=20,
        )

    def test_inventory_listing(self):

        response = self.client.get(
            f"/stores/{self.store.id}/inventory/"
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        self.assertEqual(
            len(response.data),
            1,
        )