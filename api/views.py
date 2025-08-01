from django.db.models import Max
from django.shortcuts import get_object_or_404
from api.serialaizers import ProductSerializer,OrderItemSerializer,OrderSerializer,ProductInfoSerializer
from api.models import Product,Order,OrderItem
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated,AllowAny,IsAdminUser
from rest_framework.views import APIView
from api.filters import ProductFilter,InStockFilterBackend
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters



class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.filter(stock__gt=0)
    serializer_class = ProductSerializer
    filterset_class = ProductFilter
    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter,
                       filters.OrderingFilter,
                       InStockFilterBackend]
    # filterset_fields=('name','price')
    search_fields = ['name','price']
    order_fields = ['name','stock']

    def get_permissions(self):
        self.permission_classes = [AllowAny]
        if self.request.method == "POST":
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()


# @api_view(['GET'])
# def product_list(request):
#     products = Product.objects.all()
#     serializer = ProductSerializer(products,many=True)
#     return Response(
#         serializer.data
#     ) 

# @api_view(['GET'])
# def product_detail(request,pk):
#     product = get_object_or_404(Product,id=pk)
#     serializer = ProductSerializer(product)
#     return Response(serializer.data)
    
# return single object from database
class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_url_kwarg = 'product_id'

    def get_permissions(self):
        self.permission_classes = [AllowAny]
        if self.permission_classes in ['PUT','PATCH','DELETE']:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()

# @api_view(['GET'])
# def order_list(request):
#     order = Order.objects.prefetch_related('items__product')
#     serializer = OrderSerializer(order,many=True)
#     return Response(serializer.data)

class OrderListView(generics.ListAPIView):
    queryset = Order.objects.prefetch_related('items__product')
    serializer_class = OrderSerializer

class UserOrderListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Order.objects.prefetch_related('items__product')
    serializer_class = OrderSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(user=self.request.user)


class ProductInfoApiView(APIView):
    products = Product.objects.all()
    serializer = ProductInfoSerializer({
        'products':products,
        'count': len(products),
        'max_price':products.aggregate(max_price=Max('price'))['max_price']
    })


# @api_view(['GET'])
# def product_info(request):
#     products = Product.objects.all()
#     serializer = ProductInfoSerializer({
#         'products':products,
#         'count': len(products),
#         'max_price':products.aggregate(max_price=Max('price'))['max_price']
#     })
    
#     return Response(serializer.data)