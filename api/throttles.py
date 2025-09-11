from h11 import Response
from rest_framework.throttling import SimpleRateThrottle
from rest_framework.exceptions import Throttled
from rest_framework.views import exception_handler as drf_exception_handler




class ProductBurstRateThrottle(SimpleRateThrottle):
    scope = 'products_burst'
    
    def get_cache_key(self, request, view):
        return super().get_ident(request)

class ProductSustainedRateThrottle(SimpleRateThrottle):
    scope = 'products_sustained'

    def get_cache_key(self, request, view):
        return super().get_ident(request)
    

def custom_throttle_exception_handler(exc,context):
    if isinstance(exc,context):
        wait = getattr(exc,'wait',None)
        return Response(
            {
                "detail":"there is too many requests,try another time",
                "available_in_secends":wait,
                "available_in_minutes":round(wait /60,2)
            },
            status=429,
        )
    return drf_exception_handler(exc, context)