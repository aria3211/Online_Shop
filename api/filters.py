import django_filters
from api.models import Product

class ProductFilter(django_filters.FilterSet):
    class Meta:
        model = Product
        # fields = ('name','price')
        fields = {
            'name':['exact','contains'],
            'price':['exact','gt','lt','range']
        }