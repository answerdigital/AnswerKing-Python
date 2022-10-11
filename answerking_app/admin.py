from django.contrib import admin
from answerking_app.models.models import Item, Category, Status, Order, OrderLine

admin.site.register(Item)
admin.site.register(Category)
admin.site.register(Status)
admin.site.register(Order)
admin.site.register(OrderLine)
