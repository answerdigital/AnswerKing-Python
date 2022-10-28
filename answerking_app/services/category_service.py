from django.db import IntegrityError
from django.db.models import QuerySet

from answerking_app.models.models import Category, Item
from answerking_app.models.serializers import (
    CategorySerializer,
    ItemSerializer,
)
from answerking_app.services.service_types.CategoryTypes import CategoryDict
from answerking_app.services.service_types.ItemTypes import ItemWithIDDict


def get_all() -> QuerySet[Category]:
    return Category.objects.all()


def get_by_id(cat_id: str) -> Category | None:
    try:
        cat_id_as_int: int = int(cat_id)
    except ValueError:
        return None

    try:
        category: Category = Category.objects.get(pk=cat_id_as_int)
        return category
    except Category.DoesNotExist:
        return None


def create(body: CategoryDict) -> Category | None:
    serialized_cat: CategorySerializer = CategorySerializer(data=body)
    if not serialized_cat.is_valid():
        return None

    category: Category = Category(name=serialized_cat.data["name"])
    try:
        category.save()
    except IntegrityError:
        # duplicated key name
        return None

    return update_item_list(category, serialized_cat.data.get("items", []))


def update(category: Category, body: CategoryDict) -> Category | None:
    serialized_cat: CategorySerializer = CategorySerializer(data=body)
    if not serialized_cat.is_valid():
        return None

    category.name = serialized_cat.data["name"]
    try:
        category.save()
    except IntegrityError:
        # duplicated key name
        return None

    return update_item_list(category, serialized_cat.data.get("items", []))


def update_item_list(
    category: Category, items: list[ItemWithIDDict]
) -> Category | None:
    for item in items:
        try:
            serialized_item: ItemSerializer = ItemSerializer(data=item)
            if not serialized_item.is_valid():
                return None
            category.items.add(Item.objects.get(pk=serialized_item.data["id"]))
        except Item.DoesNotExist:
            pass
    return category
