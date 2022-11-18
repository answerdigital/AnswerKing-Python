from django.contrib import admin
from answerking_app.models.models import (
    Product,
    Category,
    Order,
    OrderLine,
)

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Order)
admin.site.register(OrderLine)
