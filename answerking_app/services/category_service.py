from django.db.models import QuerySet

from answerking_app.models.models import Category, Item
from answerking_app.models.validation.serializers import (
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

    cat_name: str = serialized_cat.data["name"]
    existing: bool = Category.objects.filter(name=cat_name).exists()
    if existing:
        return None

    category: Category = Category(name=cat_name)
    category.save()

    return update_item_list(category, body["items"])


def update(category: Category, body: CategoryDict) -> Category | None:
    serialized_cat: CategorySerializer = CategorySerializer(data=body)
    if not serialized_cat.is_valid():
        return None

    try:
        existing: Category = Category.objects.get(name=serialized_cat.data["name"])
        if not category == existing:
            return None
    except Category.DoesNotExist:
        pass

    category.name = serialized_cat.data["name"]
    category.save()

    return update_item_list(category, body["items"])


def update_item_list(
    category: Category, items: list[ItemWithIDDict]
) -> Category | None:
    if items:
        for i in items:
            try:
                serialized_item: ItemSerializer = ItemSerializer(data=i)
                if not serialized_item.is_valid():
                    return None
                category.items.add(Item.objects.get(pk=i["id"]))
            except Item.DoesNotExist:
                pass
    return category
