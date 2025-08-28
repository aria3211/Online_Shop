from multiprocessing import managers
from pickletools import read_long1
from django.db import transaction
from rest_framework import serializers
from .models import Product, Order, OrderItem,User
# from django.contrib.auth.models import User



class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            'id',
            'name',
            'description',
            'price',
            'stock'
        )
    def validate_price(self, data):
        if data <=0:
            raise serializers.ValidationError('Price Must be grater than 0')
        return data

class OrderItemSerializer(serializers.ModelSerializer):
    # product = ProductSerializer()
    product_name = serializers.CharField(source='product.name',read_only=True)
    product_price = serializers.CharField(source='product.price',read_only=True)
    class Meta:
        model = OrderItem
        fields = (
            'product',
            'quiantity',
            'product_name',
            'product_price'
            )



class OrderSerializer(serializers.ModelSerializer):
    order_id = serializers.UUIDField(read_only=True)
    items = OrderItemSerializer(many=True,read_only=True)
    total_price = serializers.SerializerMethodField()
    class Meta:
        model = Order
        fields = (
            'order_id',
            'user',
            'created_at',
            'status',
            'items',
            'total_price'
        )
    def get_total_price(self,obj):
       order_items = obj.items.all()
       total = sum(order_item.item_subtotal for order_item in order_items)
       return total




class OrderCreateSerializer(serializers.ModelSerializer):
    class OrderItemCreateSerializer(serializers.ModelSerializer):
        class Meta:
            model= OrderItem
            fields= ('product', 'quantity')
    order_id = serializers.UUIDField(read_only=True)
    items = OrderItemSerializer(many=True,required=False)
    class Meta:

        model = Order
        fields = (
            'order_id',
            'user',
            'created_at',
            'status',
            'items',
        )
        extra_kwargs = {
            'user': {'read_only': True}
        }

    def update(self,instance,validated_data):
        orderitem_data = validated_data.pop('items')

        with transaction.atomic():
            instance = super().update(instance,validated_data)
            print('instance ----> : ')

            if orderitem_data is not None:
                instance.items.all().delete()
                print('Delete All old items')

                for item in orderitem_data:
                    OrderItem.objects.create(order=instance,**item)
        return instance

    
    def create(self, validated_data):
        orderitem_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)

        for item in orderitem_data:
            OrderItem.objects.create(order=order,**item)
        return order

class ProductInfoSerializer(serializers.Serializer):
    # get info of product,count & max price
    products = ProductSerializer(many=True)
    count = serializers.IntegerField()
    max_price =  serializers.FloatField()




class ListOfUsersSerializer(serializers.ModelSerializer):
    orders = serializers.SerializerMethodField()
    items = OrderItemSerializer(many=True,read_only=True)
    total_price = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        # exclude = ('password')
        fields = ("username","email","is_staff","is_superuser","total_price","items","orders")
    
    def get_orders(self,obj):
        all_orders = obj.orders.all()

        items = OrderItem.objects.filter(order__in=all_orders)
        return OrderItemSerializer(items,many=True).data

    def get_total_price(self,obj):
        last_order = obj.orders.order_by("created_at").first()  
        if last_order:
            return OrderSerializer(last_order).data.get("total_price")
        return None
class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ""

