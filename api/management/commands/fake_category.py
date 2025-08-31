import random
from decimal import Decimal

from django.core.management.base import BaseCommand
from django.utils import lorem_ipsum
from api.models import User, Product, Order, OrderItem,Category




class Command(BaseCommand):
    help = "Creates application data"
    # دسته‌ها
   


    def handle(self,*args,**kwargs):
        categories = list(Category.objects.all())

    # محصولات
        products = [
            {"name": "MacBook Pro", "price": 2500,"stock":6, "categories": [categories[0]]},
            {"name": "Dell XPS", "price": 1800,"stock":6, "categories": [categories[0]]},
            {"name": "iPhone 15", "price": 1200, "stock":4,"categories": [categories[1]]},
            {"name": "Samsung Galaxy S24", "price": 1000,"stock":6, "categories": [categories[1]]},
            {"name": "Sony WH-1000XM5", "price": 400,"stock":6, "categories": [categories[2]]},
            {"name": "AirPods Pro", "price": 250,"stock":6, "categories": [categories[2]]},
        ]

        for item in products:
            product = Product.objects.create(
                name=item["name"],
                price=item["price"],
                stock=item["stock"]
            )
            # دسته‌ها رو ست می‌کنیم
            product.category.set(item["categories"])
            # return super().handle(*args, **kwargs)