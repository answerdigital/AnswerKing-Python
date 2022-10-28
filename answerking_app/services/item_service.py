from django.db.models import QuerySet
from django.db.utils import IntegrityError

from answerking_app.models.models import Item, OrderLine
from answerking_app.models.serializers import ItemSerializer
from answerking_app.services.service_types.ItemTypes import ItemDict


def get_all() -> QuerySet[Item]:
    return Item.objects.all()


def get_by_id(item_id: str) -> Item | None:
    try:
        item_id_as_int: int = int(item_id)
    except ValueError:
        return None

    try:
        item: Item = Item.objects.get(pk=item_id_as_int)
        return item
    except Item.DoesNotExist:
        return None


def create(body: ItemDict) -> Item | None:
    serialized_item: ItemSerializer = ItemSerializer(data=body)
    if not serialized_item.is_valid():
        return None

    item: Item = Item(**serialized_item.data)
    try:
        item.save()
    except IntegrityError:
        # duplicated key name
        return None
    return item


def update(item: Item, body: ItemDict) -> Item | None:
    serialized_item: ItemSerializer = ItemSerializer(data=body)
    if not serialized_item.is_valid():
        return None

    item.name = serialized_item.data["name"]
    item.price = serialized_item.data["price"]
    item.description = serialized_item.data["description"]
    item.stock = serialized_item.data["stock"]
    item.calories = serialized_item.data["calories"]

    try:
        item.save()
    except IntegrityError:
        # duplicated key name
        return None
    return item


def delete(item: Item) -> bool:
    existing_orderitems: OrderLine = OrderLine.objects.filter(item=item.id)
    if existing_orderitems:
        return False

    item.delete()
    return True
