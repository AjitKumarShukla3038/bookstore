from django.shortcuts import render,get_object_or_404
from .models import *
from django.http import JsonResponse
import json
import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .forms import BookSearchForm




def category(request, cat):
    category = Category.objects.get(id=cat)
    products = Product.objects.filter(category=category)

    context = {
        'category': category,
        'products': products,
    }

    return render(request, 'store/category.html', context)

def home(request):
    products = Product.objects.all()

    items_per_page = 6
    paginator = Paginator(products, items_per_page)
    page = request.GET.get('page')
    products = paginator.get_page(page)


    search_form = BookSearchForm()

    # Check if a search query is provided in the request
    if request.method == 'GET':
        search_query = request.GET.get('search')

        
        if search_query:
            # Filter books by name containing the search query
            products = Product.objects.filter(name__icontains=search_query)
            # Reconfigure pagination for search results
            paginator = Paginator(products, 6)
            page = request.GET.get('page')
            products = paginator.get_page(page)

    context = {'products': products,'search_query':search_query}
    return render(request, 'store/home.html', context)


def product_detail(request, product_id):

    if request.user.is_authenticated:
        user = request.user
        order, created = Order.objects.get_or_create(user=user, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items

    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
        cartItems = order['get_cart_items']

    products = Product.objects.all()
    context = {'products': products, 'cartItems': cartItems}
    return render(request, 'store/product_detail.html', context)

    
def store(request):
    if request.user.is_authenticated:
        user = request.user
        order, created = Order.objects.get_or_create(user=user, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
        cartItems = order['get_cart_items']

    products = Product.objects.all()
    categories = Category.objects.all()

    
    items_per_page = 6
    paginator = Paginator(products, items_per_page)
    page = request.GET.get('page')
    products = paginator.get_page(page)

    search_form = BookSearchForm()
    error_message=None
    # Check if a search query is provided in the request
    if request.method == 'GET':
        search_query = request.GET.get('search')

        
        if search_query:
            # Filter books by name containing the search query
            products = Product.objects.filter(name__icontains=search_query)
            # Reconfigure pagination for search results
            paginator = Paginator(products, 6)
            page = request.GET.get('page')
            products = paginator.get_page(page)

            if not products:
                error_message = "Sorry ,Try something else!"
            

                
    context = {'products': products, 'cartItems': cartItems,'categories': categories,'search_query':search_query,'error_message': error_message}
    return render(request, 'store/store.html', context)

def cart(request):
    if request.user.is_authenticated:
        user = request.user
        order, created = Order.objects.get_or_create(user=user, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}

    context = {'items': items, 'order': order}
    return render(request, 'store/cart.html', context)


def checkout(request):
    if request.user.is_authenticated:
        user = request.user
        order, created = Order.objects.get_or_create(user=user, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}

    context = {'items': items, 'order': order}
    return render(request, 'store/checkout.html', context)

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action:', action)
    print('Product:', productId)

    user = request.user
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(user=user, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)

def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        user = request.user
        order, created = Order.objects.get_or_create(user=user, complete=False)
    else:
        # Handle the case when the user is not authenticated or implement guest order creation.
        pass

    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == float(order.get_cart_total):
        order.complete = True
    order.save()

    if order.shipping == True:
        ShippingAddress.objects.create(
            user=user,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zipcode=data['shipping']['zipcode'],
        )

    return JsonResponse('Payment done..', safe=False)




def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    return render(request, 'store/product_detail.html', {'product': product})






