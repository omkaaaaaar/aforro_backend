from rest_framework.test import APITestCase

from products.models import (
    Category,
    Product,
)


class SearchAPITest(APITestCase):

    def setUp(self):

        category = Category.objects.create(
            name="Electronics"
        )

        Product.objects.create(
            title="iPhone 15",
            price=50000,
            category=category,
        )

    def test_product_search(self):

        response = self.client.get(
            "/api/search/products/?q=iphone"
        )

        self.assertEqual(
            response.status_code,
            200,
        )

    def test_product_suggest(self):

        response = self.client.get(
            "/api/search/suggest/?q=iph"
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        self.assertTrue(
            len(response.data) > 0
        )