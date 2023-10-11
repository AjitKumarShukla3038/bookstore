from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)

admin.site.register(Cart)


class BooksAdmin(admin.ModelAdmin):
    list_display =('name','author','category','price','quantity')
    # list_filter = ('status',)
    # search_fields = ['title','author','category']
    prepopulated_fields = {'slug':('name',)}

class GenreAdmin(admin.ModelAdmin):
    list_display =('name',)
    prepopulated_fields = {'slug':('name',)}


admin.site.register(Product,BooksAdmin)
admin.site.register(Category,GenreAdmin)