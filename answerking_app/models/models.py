from decimal import Decimal

from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=200, blank=True, null=True)
    price = models.DecimalField(max_digits=18, decimal_places=2, default=0.00)
    retired = models.BooleanField(default=False, null=False)


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=200, blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    products = models.ManyToManyField(Product)
    retired = models.BooleanField(default=False, null=False)


class Order(models.Model):
    class Status(models.TextChoices):
        CREATED = "Created", "Created"
        PAID = "Paid", "Paid"
        CANCELLED = "Cancelled", "Cancelled"

    order_status = models.CharField(
        max_length=10, choices=Status.choices, default=Status.CREATED
    )
    order_total = models.DecimalField(
        max_digits=18, decimal_places=2, default=0.00
    )
    created_on = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def calculate_total(self):
        total = Decimal(0.00)
        line_items = OrderLine.objects.filter(order=self.pk).values()

        if line_items:
            for ol in line_items:
                total += ol["sub_total"]

        self.order_total = total
        self.save()


class OrderLine(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    sub_total = models.DecimalField(
        max_digits=18, decimal_places=2, default=0.00
    )

    def calculate_sub_total(self):
        self.sub_total = self.quantity * self.product.price
        self.save()

    class Meta:
        unique_together = [["order", "product"]]
