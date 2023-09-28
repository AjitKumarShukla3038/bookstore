from django import forms

class BookSearchForm(forms.Form):
    search = forms.CharField(
        label='Search Books',
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Find books...'})
    )
