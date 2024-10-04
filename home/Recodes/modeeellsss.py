from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# import random

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/')  # Optional field for product images
    stock = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.name


# Extend the user model for extra details
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.CharField(max_length=121, default='example@example.com')
    phone_number = models.CharField(max_length=15)
    address = models.TextField()

    def __str__(self):
        return self.user.username


# Order model to track past orders



class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link to the user
    created_at = models.DateTimeField(auto_now_add=True)
    
    def get_total_price(self):
        total = sum(item.product.price * item.quantity for item in self.cart_items.all())
        return total

    def __str__(self):
        return f"Cart of {self.user.username}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_items')  # Link to the Cart
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # Link to the Product
    quantity = models.PositiveIntegerField(default=1)  # Quantity of the product in the cart

    def __str__(self):
        return f"{self.product.name} (x{self.quantity})"


class Order(models.Model):
    PAYMENT_METHOD_CHOICES = [
    ('credit_card', 'Credit Card'),
    ('cod', 'Cash on Delivery'),
    ('razorpay', 'Razorpay'),  # Add Razorpay as a valid choice
]

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=255,null=False,  default='Unnamed Customer')
    email = models.EmailField(default="example@example.com")
    address = models.TextField(default='Enter Your Address')
    phone = models.CharField(max_length=15,null=False,default='Enter Phone Number')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, default='Choose payment method')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='Pending')
    # items = models.ManyToManyField(OrderItem)

    def __str__(self):
        return f"Order {self.id} by {self.name}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product.name} (x{self.quantity})"
 
 
 
    
# class OTP(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     otp = models.CharField(max_length=6)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def is_expired(self):
#         # OTP expiry time (e.g., 5 minutes)
#         return timezone.now() > self.created_at + timezone.timedelta(minutes=5)

#     @classmethod
#     def generate_otp(cls):
#         return str(random.randint(100000, 999999))    