from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.ProductListCreateView.as_view()),
    path('products/<int:product_id>/', views.ProductDetailView.as_view()),
    path('products/info/', views.ProductInfoApiView.as_view()),
    path('orders/', views.OrderListView.as_view()),
    path('order-user/', views.UserOrderListView.as_view(),name='order-user'),

]