from django import forms

class RestaurantSearchForm(forms.Form):
    search = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={
        'placeholder': 'Search by name...',
        'class': 'form-control'
    }))
    user_location = forms.CharField(max_length=50, required=False, widget=forms.HiddenInput())
