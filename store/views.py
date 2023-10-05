from django.shortcuts import render,get_object_or_404
from .models import *
from django.http import JsonResponse
import json
import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .forms import BookSearchForm,ShippingAddress
from .utils import cookieCart,cartData
from django.contrib import messages
from django.shortcuts import redirect


def category(request, cat):
    category = Category.objects.get(id=cat)
    products = Product.objects.filter(category=category)

    context = {
        'category': category,
        'products': products,
    }

    return render(request, 'store/category.html', context)

def home(request):
    products = Product.objects.all().order_by('name')

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
    data=cartData(request)
    cartItems=data['cartItems']
    order=data['order']
    items=data['items']

    products = Product.objects.all().order_by('name')
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

# def cart(request):
#     user = request.user
#     cartItems = Cart.objects.filter(user=user)
  

#     for item in cartItems:
#         total_amount=item.product.price* item.quantity
    
#     return render(request,'store/cart.html',{'items':cartItems,'order':order, 'items':items})







def checkout(request):
    cart_items = Cart.objects.filter(user=request.user)
    cart_total = 0  

    for item in cart_items:
        item.total_price = item.product.price * item.quantity  
        cart_total += item.total_price  
    return render(request, 'store/checkout.html', {'cart_items': cart_items, 'cart_total': cart_total})
    



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




def addtocart(request, product_id):

    product = get_object_or_404(Product, id=product_id)
    try:
        quantity = int(request.POST.get('quantity', 1))
        if quantity < 1:
            raise ValueError()
    except (TypeError, ValueError):
        messages.error(request, 'Please enter a valid quantity.')
        return redirect('viewcart')
    
    if quantity > product.quantity:
        return render(request, 'store/emptycart.html', {'message': 'Cannot add more items than available!'})

    user = request.user     
    created = Cart.objects.filter(user=user, product=product).first()
    
    if created:
        created.quantity += quantity
        created.save()
    else:
        cart_item = Cart(user=user,product=product,quantity=quantity)
        cart_item.save()
    
    product.quantity -= quantity
    product.save()
    
    return redirect('store') 
    


def cart(request):


    cart_items = Cart.objects.filter(user=request.user)
    cart_total = 0  

    for item in cart_items:
        item.total_price = item.product.price * item.quantity  
        cart_total += item.total_price  
    return render(request, 'store/cart.html', {'cart_items': cart_items, 'cart_total': cart_total})


def update_cart(request, cart_item_id):
    cart_item = Cart.objects.get(pk=cart_item_id)
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity'))
        if quantity <= 0:
            messages.error(request, 'Please enter a valid quantity.')

        elif quantity > cart_item.product.quantity:
            messages.error(request, 'The requested quantity exceeds the available quantity.')

        else:
            new_quantity = quantity - cart_item.quantity
            cart_item.quantity = quantity
            cart_item.save()
            cart_item.product.quantity  -= new_quantity
            cart_item.product.save()
    return redirect('cart')
		


def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(Cart, pk=cart_item_id, user=request.user)
    
    if cart_item.user == request.user:
        cart_quantity = cart_item.quantity
        product = cart_item.product
        
        cart_item.delete()
        product.quantity += cart_quantity
        product.save()
    return redirect('cart')


