from django.shortcuts import render,get_object_or_404
from .models import *
from django.http import JsonResponse
import json
import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .forms import BookSearchForm,ShippingAddressForm
from .utils import cookieCart,cartData
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required 


def category(request, slug):
    category = Category.objects.get(slug=slug)
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


# def product_detail(request, slug):

#     if request.user.is_authenticated:
#         user = request.user
#         order, created = Order.objects.get_or_create(user=user, complete=False)
#         items = order.orderitem_set.all()
#         cartItems = order.get_cart_items

#     else:
#         items = []
#         order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
#         cartItems = order['get_cart_items']

#     products = Product.objects.all(slug=slug)
#     context = {'products': products, 'cartItems': cartItems}
#     return render(request, 'store/product_detail.html', context)

    
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







@login_required
def checkout(request):


    cart_items = Cart.objects.filter(user=request.user)
    user_default_address = ShippingAddress.objects.filter(user=request.user, is_default=True).first()

    cart_total = 0  

    for item in cart_items:
        item.total_price = item.product.price * item.quantity  
        cart_total += item.total_price  


    if request.method=='POST':
        form=ShippingAddressForm(request.POST)
        if form.is_valid():
            shipping_address = form.save(commit=False)
            shipping_address.user = request.user
            shipping_address.save()
            messages.success(request, 'Address saved successfully.')
            return redirect('checkout')
        else:
            pass
    else:
            
        form_data = {'user_default_address': True} if user_default_address else {}
        form = ShippingAddressForm(initial=form_data)

    
    
    return render(request, 'store/checkout.html', {'cart_items': cart_items, 'cart_total': cart_total,'form': form,'user_default_address': user_default_address})
    

@login_required
def process_payment(request):
    cart_items = Cart.objects.filter(user=request.user)

    if not cart_items.exists():
        messages.error(request, 'Your cart is empty. Please add items to proceed with the payment.')
        return redirect('cart')  # Redirect to the cart page or any other appropriate page
        
    orders = Order.objects.filter(user=request.user)
    messages.success(request, 'payment saved successfully.')
        
    cart_items.delete()



    return render(request, 'order_history.html', {'orders': orders})




def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    return render(request, 'store/product_detail.html', {'product': product})



@login_required
def addtocart(request, product_id):

    product = get_object_or_404(Product, id=product_id)
    try:
        quantity = int(request.POST.get('quantity', 1))
        if quantity < 1:
            raise ValueError()
    except (TypeError, ValueError):
        messages.error(request, 'Please enter a valid quantity.')
        return redirect('cart')
    
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



