from django.urls import path
from . import views
from rest_framework import routers



urlpatterns = [
    path('products/', views.ProductListCreateView.as_view(),name='products'),
    path('products/<int:product_id>/', views.ProductDetailView.as_view(),name='product_detail'),
    path('products/info/', views.ProductInfoApiView.as_view()),
    path('users/', views.ListOfUsersView.as_view()),
    path('categories/', views.CategoryInfoView.as_view(),name='categories'),
    # path('orders/', views.OrderListView.as_view()),
    # path('order-user/', views.UserOrderListView.as_view(),name='order-user'),

]

router = routers.DefaultRouter()
router.register('orders',views.OrderViewSet)
urlpatterns += router.urls