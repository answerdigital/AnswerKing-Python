from decimal import Decimal

from django.db import models
from rest_framework.fields import CharField, DecimalField, IntegerField


class Item(models.Model):
    name: str = models.CharField(max_length=50)
    price: Decimal = models.DecimalField(max_digits=18, decimal_places=2, default=0.00)
    description: str = models.CharField(max_length=200, blank=True, null=True)
    stock: int = models.IntegerField(default=0)
    calories: int = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Category(models.Model):
    name: str = models.CharField(max_length=50)
    items: Item = models.ManyToManyField(Item)

    def __str__(self) -> str:
        return self.name


class Status(models.Model):
    status = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.status


class Order(models.Model):
    status: Status = models.ForeignKey(Status, on_delete=models.CASCADE)
    address: str = models.CharField(max_length=200)
    total: Decimal = models.DecimalField(max_digits=18, decimal_places=2, default=0.00)
    order_items: 'OrderLine' = models.ManyToManyField(Item, through="OrderLine")

    def __str__(self) -> str:
        return self.address

    def calculate_total(self) -> None:
        total: Decimal = Decimal(0.00)
        orderlines: OrderLine = OrderLine.objects.filter(order=self.pk).values()

        if orderlines:
            for ol in orderlines:
                total += ol["sub_total"]

        self.total = total
        self.save()


class OrderLine(models.Model):
    order: Order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item: Item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity: IntegerField = models.IntegerField(default=0)
    sub_total: DecimalField = models.DecimalField(max_digits=18, decimal_places=2, default=0.00)

    class Meta:
        unique_together = [["order", "item"]]
