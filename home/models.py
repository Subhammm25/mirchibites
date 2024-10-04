from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime
import pytz


# Product model to store product details
class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/')  # Optional field for product images
    stock = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


# UserProfile model to extend user details with email, phone, and address
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(default='example@example.com')
    phone_number = models.CharField(max_length=15)
    address = models.TextField()

    def __str__(self):
        return self.user.username


# Cart model to store products added to the user's cart
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link to the user
    created_at = models.DateTimeField(auto_now_add=True)

    def get_total_price(self):
        total = sum(item.product.price * item.quantity for item in self.cart_items.all() if item.product.price and item.quantity)
        return total

    def __str__(self):
        return f"Cart of {self.user.username}"


# CartItem model to represent individual products in the cart
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_items')  # Link to the Cart
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # Link to the Product
    quantity = models.PositiveIntegerField(default=1)  # Quantity of the product in the cart

    def __str__(self):
        return f"{self.product.name} (x{self.quantity})"


# Order model to represent placed orders
class Order(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('credit_card', 'Credit Card'),
        ('cod', 'Cash on Delivery'),
        ('razorpay', 'Razorpay'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=255, null=False, default='Unnamed Customer')
    email = models.EmailField(default="example@example.com")
    address = models.TextField(default='Enter Your Address')
    phone = models.CharField(max_length=15, null=False, default='Enter Phone Number')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, default='razorpay')  # Updated default
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='Pending')

    def __str__(self):
        return f"Order {self.id} by {self.name}"

    # Calculate the total price of the order based on associated items
    def get_order_total(self):
        return sum(item.price * item.quantity for item in self.items.all())


# OrderItem model to represent individual items in an order
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product.name} (x{self.quantity})"


# Automatically create and save a UserProfile when a new user is created
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()

