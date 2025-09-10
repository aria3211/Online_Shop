from django.db.models import Max
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.vary import vary_on_headers
from django.views.decorators.cache import cache_page
from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, pagination
from rest_framework.decorators import action, api_view
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from api.filters import InStockFilterBackend, OrderFilter, ProductFilter
from api.models import Category, Order, OrderItem, Product, User
from api.serialaizers import (ListOfUsersSerializer, OrderItemSerializer,
                              OrderSerializer, ProductInfoSerializer,
                              ProductSerializer,OrderCreateSerializer,ListCategorySerializer)

# from django.contrib.auth.models import User


class ProductListCreateView(generics.ListCreateAPIView):
    # queryset = Product.objects.filter(stock__gt=0)
    queryset = Product.objects.order_by('pk')
    serializer_class = ProductSerializer
    filterset_class = ProductFilter
    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter,
                       filters.OrderingFilter,
                       InStockFilterBackend,]
    # filterset_fields=('name','price')
    search_fields = ['name','price']
    order_fields = ['name','stock']

    # pagination with pagenumberpagination
    ''' pagination_class = pagination.PageNumberPagination
    pagination_class.page_size = 5
    pagination_class.page_query_param = 'Pagenumber'
    pagination_class.page_size_query_param = 'size'
    pagination_class = 10  '''
    pagination_class = pagination.LimitOffsetPagination

    @method_decorator(cache_page(60*15,key_prefix='product_list'))
    @method_decorator(vary_on_headers("Authorization"))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    def get_queryset(self):
        import time
        time.sleep(2)
        return super().get_queryset()


    def get_permissions(self):
        self.permission_classes = [AllowAny]
        if self.request.method == "POST":
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()

class ListOfUsersView(generics.ListAPIView):
    queryset = User.objects.all()
    pagination_class = None

    serializer_class = ListOfUsersSerializer

    # def get_password(self):
    #     self.


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
    
# adding viewset for ordering
class OrderViewSet(ModelViewSet):
    queryset = Order.objects.prefetch_related('items__product')
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None
    filterset_class = OrderFilter
    filter_backends = [DjangoFilterBackend]

    @method_decorator(cache_page(60*15,key_prefix='product_list'))
    @method_decorator(vary_on_headers("Authorization"))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    
    def get_serializer_class(self):
        if self.action =='create' or self.action == 'update':
            return OrderCreateSerializer
        return super().get_serializer_class()

    def get_queryset(self):
        qs = super().get_queryset()
        if not self.request.user.is_staff:
            qs = qs.filter(user=self.request.user)
        return qs

    @action(detail=False,methods=['get'],url_path='user_orders',permission_classes=[IsAuthenticated])
    def user_orders(self,request):
        orders = self.get_queryset().filter(user=request.user)
        serializer = self.get_serializer(orders,many=True)
        return Response(serializer.data)





'''
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

'''
class ProductInfoApiView(APIView):
    products = Product.objects.all()
    serializer = ProductInfoSerializer({
        'products':products,
        'count': len(products),
        'max_price':products.aggregate(max_price=Max('price'))['max_price']
    })

class CategoryInfoView(generics.ListCreateAPIView):
    queryset = Category.objects.annotate(product__count=Count('products'))
    serializer_class = ListCategorySerializer

    @method_decorator(cache_page(60*10,key_prefix="category_list"))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    def get_queryset(self):
        import time
        time.sleep(5)
        return super().get_queryset()
        
# @api_view(['GET'])
# def product_info(request):
#     products = Product.objects.all()
#     serializer = ProductInfoSerializer({
#         'products':products,
#         'count': len(products),
#         'max_price':products.aggregate(max_price=Max('price'))['max_price']
#     })
    
#     return Response(serializer.data)
    
