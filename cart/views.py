import json
import requests
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from account.models import Address
from .cart_module import Cart
from product.models import Product
from .models import Order, OrderItem, DiscountCode
from .wishlist_module import WishList

# ? sandbox merchant
if settings.SANDBOX:
    sandbox = 'sandbox'
else:
    sandbox = 'www'

ZP_API_REQUEST = f"https://{sandbox}.zarinpal.com/pg/services/WebGate/wsdl"
ZP_API_VERIFY = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentVerification.json"
ZP_API_STARTPAY = f"https://{sandbox}.zarinpal.com/pg/StartPay/"

amount = 1000  # Rial / Required
description = "توضیحات مربوط به تراکنش را در این قسمت وارد کنید"  # Required
phone = 'YOUR_PHONE_NUMBER'  # Optional
# Important: need to edit for realy server.
CallbackURL = 'http://127.0.0.1:8080/cart/verify/'


class CartDetailView(View):
    def get(self, request):
        cart = Cart(request)
        return render(request, 'cart/cart.html', {'cart': cart})


class CartAddView(View):
    def post(self, request, pk):
        product = get_object_or_404(Product, id=pk)
        size, quantity = request.POST.get('size'), request.POST.get('quantity')
        cart = Cart(request)
        cart.add(product, quantity, size)
        return redirect('cart:cart-detail')


class CartDeleteView(View):
    def get(self, request, id):
        cart = Cart(request)
        cart.delete(id)
        return redirect('cart:cart-detail')


class OrderDetailView(LoginRequiredMixin, View):
    def get(self, request, pk):
        order = get_object_or_404(Order, id=pk)
        return render(request, 'cart/order_detail.html', {'order': order})


class OrderCreationView(LoginRequiredMixin, View):
    def get(self, request):
        cart = Cart(request)
        order = Order.objects.create(user=request.user, total_price=cart.total())

        for item in cart:
            OrderItem.objects.create(order=order, product=item['product'], size=item['size'],
                                     quantity=item['quantity'], price=item['price'])
            order.products.add(item['product'])

        cart.remove_cart()

        return redirect('cart:order-detail', order.id)


class DiscountCodeView(View):
    def post(self, request, pk):
        order = get_object_or_404(Order, id=pk)

        if order.discount_code:
            return redirect('cart:order-detail', order.id)

        code = request.POST.get('discount_code')
        discount_code = get_object_or_404(DiscountCode, name=code)

        if discount_code.quantity == 0:
            discount_code.delete()
            return redirect('cart:order-detail', order.id)

        order.total_price -= order.total_price * discount_code.discount / 100

        order.discount_code = discount_code
        order.save()
        discount_code.quantity -= 1
        discount_code.save()

        return redirect('cart:order-detail', order.id)


class SendRequestView(View):

    def post(self, request, pk):
        order = get_object_or_404(Order, id=pk, user=request.user)
        address = get_object_or_404(Address, id=request.POST.get('address'))
        order.address = f'{address.address} - {address.phone}'
        order.save()
        request.session['order_id'] = str(order.id)

        data = {
            "MerchantID": settings.MERCHANT,
            "Amount": amount,
            "Description": description,
            "Phone": address.phone,
            "CallbackURL": CallbackURL,
        }
        data = json.dumps(data)
        headers = {'content-type': 'application/json', 'content-length': str(len(data))}
        try:
            response = requests.post(ZP_API_REQUEST, data=data, headers=headers, timeout=10)

            if response.status_code == 200:
                response = response.json()
                if response['Status'] == 100:
                    return JsonResponse({'status': True, 'url': ZP_API_STARTPAY + str(response['Authority']),
                                         'authority': response['Authority']})
                else:
                    return JsonResponse({'status': False, 'code': str(response['Status'])})
            return JsonResponse({'status': False, 'code': response.status_code})

        except requests.exceptions.Timeout:
            return JsonResponse({'status': False, 'code': 'timeout'})
        except requests.exceptions.ConnectionError:
            return JsonResponse({'status': False, 'code': 'connection error'})


def verify(request, authority):
    order_id = request.session['order_id']
    order = Order.objects.get(id=int(order_id))
    data = {
        "MerchantID": settings.MERCHANT,
        "Amount": order.total_price,
        "Authority": authority,
    }
    data = json.dumps(data)
    # set content length by data
    headers = {'content-type': 'application/json', 'content-length': str(len(data))}
    response = requests.post(ZP_API_VERIFY, data=data, headers=headers)

    if response.status_code == 200:
        response = response.json()
        if response['Status'] == 100:
            order.is_paid = True
            order.save()
            return render(request, 'cart/cart_verify.html')
        else:
            return {'status': False, 'code': str(response['Status'])}
    return response


class WishListDetailView(View):
    def get(self, request):
        wishlist = WishList(request)
        return render(request, 'cart/wishlist.html', {'wishlist': wishlist})


class WishListAddView(View):
    def post(self, request, pk):
        product = get_object_or_404(Product, id=pk)
        size, quantity = request.POST.get('size', 'کوچک'), request.POST.get('quantity', 1)
        wishlist = WishList(request)
        wishlist.add(product, quantity)
        return redirect('cart:wishlist')


class WishListDeleteView(View):
    def get(self, request, product_id, size=None):
        wishlist = WishList(request)
        wishlist.delete_item(product_id, size)
        return redirect('cart:wishlist')
