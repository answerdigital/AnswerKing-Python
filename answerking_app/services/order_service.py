from decimal import Decimal, InvalidOperation

from django.core.exceptions import ValidationError
from django.db import DataError
from django.db.models import QuerySet

from answerking_app.models.models import Item, Order, Status
from answerking_app.models.serializers import OrderSerializer
from answerking_app.services.service_types.OrderTypes import (OrderCreateDict,
                                                              OrderItems,
                                                              OrderUpdateDict)


def get_all() -> QuerySet[Order]:
    return Order.objects.all()


def get_by_id(order_id: str) -> Order | None:
    try:
        order_id_as_int: int = int(order_id)
    except ValueError:
        return None

    try:
        order: Order = Order.objects.get(pk=order_id_as_int)
        return order
    except Order.DoesNotExist:
        return None


def create(body: OrderCreateDict) -> Order | None:
    serialized_order = OrderSerializer(data=body)
    if not serialized_order.is_valid():
        return None
    status, _ = Status.objects.get_or_create(status="Pending")

    created_order: Order = Order(
        address=serialized_order.data["address"], status=status, total=0.00
    )
    created_order.save()

    try:
        if not serialized_order.data["order_items"]:
            return created_order
    except KeyError:
        return created_order

    for oi in serialized_order.data["order_items"]:
        try:
            try:
                # note for tommorrow, id doesn not exist in the oi object
                item: Item = Item.objects.get(pk=oi["id"])
                quantity: int = int(oi["quantity"])
                price: Decimal = item.price
                stock: int = item.stock
                sub_total: Decimal = Decimal(quantity * price)
            except (KeyError, InvalidOperation, ValueError) as e:
                created_order.delete()
                return None

            if quantity > stock:
                created_order.delete()
                return None

            created_order.order_items.add(
                item,
                through_defaults={
                    "quantity": quantity,
                    "sub_total": sub_total,
                },
            )
        except Item.DoesNotExist:
            pass

    created_order.calculate_total()

    return created_order


def update(order: Order, body: OrderUpdateDict) -> Order | None:
    try:
        address: str = validate_address_string(body["address"])
        order.address = address
    except ValidationError:
        return None
    except KeyError:
        pass

    try:
        updated_status: str = body["status"]
        status: Status = Status.objects.get(status=updated_status)
        order.status = status
    except Status.DoesNotExist:
        return None
    except KeyError:
        pass

    order.save()

    return order


def add_item(order: Order, item: Item, quantity: int) -> Order | None:
    if quantity == 0:
        return remove_item(order, item)

    if item not in order.order_items.all():
        try:
            order.order_items.add(
                item,
                through_defaults={
                    "quantity": quantity,
                    "sub_total": sub_total,
                },
            )
        except DataError:
            return None
    else:
        try:
            order.orderline_set.filter(item=item.id).update(
                quantity=quantity, sub_total=sub_total
            )
        except DataError:
            return None

    order.calculate_total()
    return order


def remove_item(order: Order, item: Item) -> Order:
    order.order_items.remove(item)
    order.calculate_total()
    return order
