from decimal import Decimal

from django.db import models


class Item(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=18, decimal_places=2, default=0.00)
    description = models.CharField(max_length=200, blank=True, null=True)
    stock = models.IntegerField(default=0)
    calories = models.IntegerField(default=0)

    def __str__(self) -> str:
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=50)
    items = models.ManyToManyField(Item)

    def __str__(self) -> str:
        return self.name


class Status(models.Model):
    status = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.status


class Order(models.Model):
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    address = models.CharField(max_length=200)
    total = models.DecimalField(max_digits=18, decimal_places=2, default=0.00)
    order_items = models.ManyToManyField(Item, through="OrderLine")

    def __str__(self) -> str:
        return self.address

    def calculate_total(self):
        total = Decimal(0.00)
        orderlines = OrderLine.objects.filter(order=self.pk).values()

        if orderlines:
            for ol in orderlines:
                total += ol["sub_total"]

        self.total = total
        self.save()


class OrderLine(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    sub_total = models.DecimalField(max_digits=18, decimal_places=2, default=0.00)

    class Meta:
        unique_together = [["order", "item"]]
