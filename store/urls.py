from django.urls import path

from . import views
urlpatterns = [
	path('', views.store, name="store"),
	path('cart/', views.cart, name="cart"),
	path('checkout/', views.checkout, name="checkout"),
    path('update_item/', views.updateItem, name="update_item"),
	path('process_order/', views.processOrder, name="process_order"),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
	path('store/<int:page>/', views.store, name='store_with_pagination'),  # Add this line

    path('home/', views.home, name="home"),
    path('category/<int:cat>/', views.category, name="category"),

    path('addtocart/<int:product_id>',views.addtocart,name='addtocart'),
    path('update_cart/<int:cart_item_id>/', views.update_cart,name='update_cart'),
    path('remove_from_cart/<int:cart_item_id>',views.remove_from_cart,name='remove_from_cart'),
    # path('add_address',views.add_shipping_address,name='add_address'),

]