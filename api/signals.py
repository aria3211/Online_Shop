from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from api.models import Category, Product
from django.core.cache import cache



@receiver([post_save,post_delete],sender=Product)
def invalidate_product_cache(sender,instance,**kwargs):
    """
    Invalidate product list caches when a product is created, updated, or deleted
    """
    print("Clearing product cache")
    cache.delete_pattern('*product_list*')


@receiver([post_save,post_delete],sender=Product)
def invalidate_category_cache(sender,instance,**kwargs):
    print("Clearing category cache")
    cache.delete_pattern("*category_list*")