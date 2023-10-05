from django import forms
from .models import ShippingAddress

class BookSearchForm(forms.Form):
    search = forms.CharField(
        label='Search Books',
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Find books...'})
    )



# class UpdateCartForm(forms.ModelForm):
#     class Meta:
#         model = Cart
#         fields = ['quantity']


class ShippingAddress(forms.ModelForm):
	class Meta:
		model = ShippingAddress
		fields = ['address', 'city', 'state', 'zipcode']