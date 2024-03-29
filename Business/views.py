import datetime
import json

from django.shortcuts import render
from django.http import JsonResponse
from .models import *
from .utils import cookieCart, cartData


# Create your views here.


def store(request):
    data = cartData(request)
    cartItems = data['cartItems']
    # items = data['items']
    # order = data['order']

    products = Product.objects.all()
    context = {
        'products': products,
        'cartItems': cartItems,

    }
    return render(request, 'stores/store.html', context)


def cart(request):

    data = cartData(request)
    cartItems = data['cartItems']
    items = data['items']
    order = data['order']
    context = {
        'items': items,
        'order': order,
        'cartItems': cartItems,
    }
    return render(request, 'stores/cart.html', context)


def checkout(request):

    data = cartData(request)
    cartItems = data['cartItems']
    items = data['items']
    order = data['order']

    context = {
        'items': items,
        'order': order,
        'cartItems': cartItems,
    }
    return render(request, 'stores/checkout.html', context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action:', action)
    print("ProductID:", productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()
    return JsonResponse('Item was added...', safe=False)


def processOrder(request):
    # print('Data:', request.body)
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        total = float(data['form']['total'])
        order.transaction_id = transaction_id

        if total == order.get_cart_total:
            order.complete = True

        order.save()

        if order.shipping:
            ShippingAddress.objects.create(
                customer=customer,
                order=order,
                address=data['shipping']['address'],
                city=data['shipping']['city'],
                state=data['shipping']['state'],
                zipcode=data['shipping']['zipcode']
            )

    return JsonResponse('Payment complete!...', safe=False)
