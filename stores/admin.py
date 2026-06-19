from django.contrib import admin
from .models import Store, Inventory


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "location",
    )

    search_fields = (
        "name",
        "location",
    )


@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "store",
        "product",
        "quantity",
    )

    search_fields = (
        "store__name",
        "product__title",
    )

    list_filter = ("store",)