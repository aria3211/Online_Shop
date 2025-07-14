from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.ProductListView.as_view()),
    path('products/<int:product_id>/', views.ProductDetailView.as_view()),
    path('products/info/', views.product_info),
    path('orders/', views.OrderListView.as_view()),
    path('order-user/', views.UserOrderListView.as_view()),

]