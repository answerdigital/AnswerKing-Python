from answerking_app.models.models import Category, Item
from answerking_app.models.validation.serializers import (
    CategorySerializer,
    ItemSerializer,
)


def get_all():
    categories = Category.objects.all()

    if not categories:
        return []

    return categories


def get_by_id(cat_id):
    try:
        cat_id = int(cat_id)
    except ValueError:
        return None

    try:
        category = Category.objects.get(pk=cat_id)
        return category
    except Category.DoesNotExist:
        return None


def create(body):
    serialized_cat = CategorySerializer(data=body)
    if not serialized_cat.is_valid():
        return None

    cat_name = serialized_cat.data["name"]
    existing = Category.objects.filter(name=cat_name).exists()
    if existing:
        return None

    category = Category(name=cat_name)
    category.save()

    return update_item_list(category, body["items"])


def update(category, body):
    serialized_cat = CategorySerializer(data=body)
    if not serialized_cat.is_valid():
        return None

    try:
        existing = Category.objects.get(name=serialized_cat.data["name"])
        if not category == existing:
            return None
    except Category.DoesNotExist:
        pass

    category.name = serialized_cat.data["name"]
    category.save()

    return update_item_list(category, body["items"])


def update_item_list(category, items):
    if items:
        for i in items:
            try:
                serialized_item = ItemSerializer(data=i)
                if not serialized_item.is_valid():
                    return None
                category.items.add(Item.objects.get(pk=i["id"]))
            except Item.DoesNotExist:
                pass
    return category
