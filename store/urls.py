from django.urls import path

from . import views
urlpatterns = [
	path('', views.store, name="store"),
	path('cart/', views.cart, name="cart"),
	path('checkout/', views.checkout, name="checkout"),
    # path('update_item/', views.updateItem, name="update_item"),
	# path('process_order/', views.processOrder, name="process_order"),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
	path('store/<int:page>/', views.store, name='store_with_pagination'),  # Add this line

    path('home/', views.home, name="home"),
    path('category/<slug:slug>/', views.category, name="category"),

    path('addtocart/<int:product_id>',views.addtocart,name='addtocart'),
    path('update_cart/<int:cart_item_id>/', views.update_cart,name='update_cart'),
    path('remove_from_cart/<int:cart_item_id>',views.remove_from_cart,name='remove_from_cart'),
    path('process_payment/', views.process_payment, name='process_payment'),

]

