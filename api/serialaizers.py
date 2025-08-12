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
    product_name = serializers.CharField(source='product.name')
    product_price = serializers.CharField(source='product.price')
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


class ProductInfoSerializer(serializers.Serializer):
    # get info of product,count & max price
    products = ProductSerializer(many=True)
    count = serializers.IntegerField()
    max_price =  serializers.FloatField()


class ListOfUsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
