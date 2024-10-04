from django import forms
from .models import Order
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['name', 'email', 'address', 'phone', 'payment_method']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Full Name', 'class': 'input-field'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email Address', 'class': 'input-field'}),
            'address': forms.Textarea(attrs={'placeholder': 'Shipping Address', 'class': 'input-field', 'rows': 3}),
            'phone': forms.TextInput(attrs={'placeholder': 'Phone Number', 'class': 'input-field'}),
            'payment_method': forms.RadioSelect(attrs={'class': 'payment-options'}),
        }



class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    number = forms.CharField(max_length=10, required=True)
    

    class Meta:
        model = User
        fields = ['username', 'email', 'number', 'password1', 'password2']