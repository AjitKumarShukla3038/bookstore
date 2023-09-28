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
    # path('home/<int:page>/', views.home, name='home_with_pagination'),  # Add this line

    path('home/', views.home, name="home"),
    path('category/<int:cat>/', views.category, name="category"),
    # path('profile/', views.profile, name='profile'),

]