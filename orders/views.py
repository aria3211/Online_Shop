from django.shortcuts import render,get_object_or_404,redirect
from django.views import View
from .cart import Cart
from .forms import CartFrom
from home.models import Product
from orders.models import OrderItem,Order
from django.contrib.auth.mixins import LoginRequiredMixin
from .tasks import order_created
class CartView(View):
    def get(self,request):
        cart = Cart(request)
        return render(request,'orders/cart.html',{'cart':cart})

class CartAddView(View):
    def post(self,request,product_id):
        cart = Cart(request)
        product = get_object_or_404(Product,id=product_id)
        form = CartFrom(request.POST)
        if form.is_valid():
            cart.add(product,form.cleaned_data['quantity'])
        return redirect('orders:cart')


class CartRemoveView(View):
    def get(self,request,product_id):
        cart = Cart(request)
        product = get_object_or_404(Product,id=product_id)
        cart.delete(product)
        return redirect('orders:cart')

class CartDecrementView(View):
    def get(self,request,product_id):
        cart = Cart(request)
        product = get_object_or_404(Product,id=product_id)
        cart.decrement(product)
        return redirect('orders:cart')
class CartincrementView(View):
    def get(self,request,product_id):
        cart = Cart(request)
        product = get_object_or_404(Product,id=product_id)
        cart.incriment(product)
        return redirect('orders:cart')


class DetailOrderView(LoginRequiredMixin,View):
    def get(self,request,order_id):
        order = get_object_or_404(Order,id=order_id)
        return render(request,'orders/order.html',{'order':order})


class CreateOrderView(LoginRequiredMixin,View):
    def get(self,request):
        cart = Cart(request)
        order = Order.objects.create(user=request.user)
        for item in cart:
            OrderItem.objects.create(order=order,product=item['product'],price=item['price'],quantity=item['quantity'])
        cart.clear()
        order_created.delay(order.id)
        return redirect('orders:order_detail',order.id)

