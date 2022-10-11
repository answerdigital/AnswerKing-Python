from answerking_app.models.models import Item, Order, OrderLine
from answerking_app.models.validation.serializers import ItemSerializer


def get_all():
    items = Item.objects.all()

    if not items:
        return []

    return items


def get_by_id(item_id):
    try:
        item_id = int(item_id)
    except ValueError:
        return None

    try:
        item = Item.objects.get(pk=item_id)
        return item
    except Item.DoesNotExist:
        return None


def create(body):
    serialized_item = ItemSerializer(data=body)
    if not serialized_item.is_valid():
        return None

    existing = Item.objects.filter(name=serialized_item.data["name"]).exists()
    if existing:
        return None

    item = Item(**serialized_item.data)
    item.save()

    return item


def update(item, body):
    serialized_item = ItemSerializer(data=body)
    if not serialized_item.is_valid():
        return None

    try:
        existing = Item.objects.get(name=serialized_item.data["name"])
        if not item == existing:
            return None
    except Item.DoesNotExist:
        pass

    item.name = serialized_item.data["name"]
    item.price = serialized_item.data["price"]
    item.description = serialized_item.data["description"]
    item.stock = serialized_item.data["stock"]
    item.calories = serialized_item.data["calories"]
    item.save()

    return item


def delete(item):
    existing_orderitems = OrderLine.objects.filter(item=item.id)
    if existing_orderitems:
        return False

    item.delete()
    return True
