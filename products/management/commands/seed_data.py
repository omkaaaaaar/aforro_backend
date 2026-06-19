import random

from django.core.management.base import BaseCommand

from faker import Faker

from products.models import (
    Category,
    Product,
)

from stores.models import (
    Store,
    Inventory,
)


class Command(BaseCommand):

    help = "Generate sample data"

    def handle(self, *args, **kwargs):

        fake = Faker()

        self.stdout.write(
            self.style.SUCCESS(
                "Creating categories..."
            )
        )

        categories = []

        category_names = [
            "Electronics",
            "Fashion",
            "Books",
            "Sports",
            "Home",
            "Beauty",
            "Automotive",
            "Health",
            "Gaming",
            "Toys",
            "Food",
            "Office",
        ]

        for name in category_names:

            category, _ = (
                Category.objects.get_or_create(
                    name=name
                )
            )

            categories.append(category)

        self.stdout.write(
            self.style.SUCCESS(
                "Creating products..."
            )
        )

        products = []

        for _ in range(1200):

            product = Product.objects.create(
                title=fake.unique.sentence(
                    nb_words=3
                )[:255],
                description=fake.text(
                    max_nb_chars=200
                ),
                price=round(
                    random.uniform(
                        100,
                        100000
                    ),
                    2,
                ),
                category=random.choice(
                    categories
                ),
            )

            products.append(product)

        self.stdout.write(
            self.style.SUCCESS(
                "Creating stores..."
            )
        )

        stores = []

        for _ in range(25):

            store = Store.objects.create(
                name=fake.company(),
                location=fake.city(),
            )

            stores.append(store)

        self.stdout.write(
            self.style.SUCCESS(
                "Creating inventory..."
            )
        )

        for store in stores:

            store_products = random.sample(
                products,
                300
            )

            inventory_rows = []

            for product in store_products:

                inventory_rows.append(
                    Inventory(
                        store=store,
                        product=product,
                        quantity=random.randint(
                            0,
                            500
                        ),
                    )
                )

            Inventory.objects.bulk_create(
                inventory_rows
            )

        self.stdout.write(
            self.style.SUCCESS(
                "Seed data created successfully."
            )
        )