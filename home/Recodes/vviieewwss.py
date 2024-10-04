from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import logout,authenticate,login
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .models import Product
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import UserProfile, Order
from .models import Cart
from .models import CartItem 
from .models import Order, OrderItem
from .forms import CheckoutForm
from django.contrib.auth.decorators import login_required
from decimal import Decimal
from .models import Cart
from .models import Order
import razorpay
from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse




from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.shortcuts import render
from .models import Order, OrderItem
from django.contrib.auth.decorators import login_required

import logging




import razorpay
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.db import transaction

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Cart, Order, OrderItem



from .forms import RegistrationForm  # Assuming you have a registration form


def home(request):

    return render(request,"home.html")
    


def loginuser(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            # Here you can check for specific cases:
            if not User.objects.filter(username=username).exists():
                messages.error(request, "No account found with this username.")
            else:
                messages.error(request, "Invalid username or password.")
  
    return render(request, 'login.html')
    
    


def registration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        
        if form.is_valid():
            # Check if the username or email already exists
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username is already taken. Please choose another one.')
                return render(request, 'registration.html', {'form': form})
            
            if User.objects.filter(email=email).exists():
                messages.error(request, 'An account with this email already exists.')
                return render(request, 'registration.html', {'form': form})
            
            # Create user but don't activate yet
            user = form.save(commit=False)
            user.is_active = False  # Set the user as inactive
            user.save()

            

           
        else:
            # Show form errors
            for field in form.errors:
                error_message = f"{field}: {form.errors[field][0]}"
                messages.error(request, error_message)

    else:
        form = RegistrationForm()

    return render(request, 'registration.html', {'form': form})

           
           
def product_list(request):
    products = Product.objects.all()  # Get all products
    return render(request, 'product_list.html', {'products': products})           

def order_product(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, 'order_product.html', {'product': product})

def our_story(request):
    return render(request,"our_story.html")

def chef_special(request):
    return render(request,"chef_special.html")

def catering(request):
    return render(request,"catering.html")



# User profile view
@login_required
def profile_view(request):
    user = request.user
    try:
        # Try to get the user profile
        user_profile = UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        # If the profile doesn't exist, create one
        user_profile = UserProfile.objects.create(user=user)

    # Fetch the past orders
    # past_orders = Order.objects.filter(user=user).order_by('-order_date')

    context = {
        'user_profile': user_profile,
        'past_orders': past_orders
    }
    return render(request, 'profile.html', context)





# View Cart
@login_required
def view_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.cart_items.all()
    print(f"Cart Items Count: {cart_items.count()}")  # Debugging output
    return render(request, 'cart.html', {'cart_items': cart_items})



# Add to Cart
@login_required
def add_to_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity', 1))

        # Check if product_id is valid
        if not product_id:
            messages.error(request, "Product ID is missing.")
            return redirect('product_list')

        # Get the product
        product = get_object_or_404(Product, id=product_id)

        # Convert product price to Decimal (if it's not already)
        product_price = Decimal(product.price)

        # Get or create the user's cart
        cart, created = Cart.objects.get_or_create(user=request.user)

        # Update or create the cart item
        cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not item_created:
            cart_item.quantity += quantity  # Update quantity if it already exists
        else:
            cart_item.quantity = quantity  # Set quantity if it's a new item

        cart_item.save()

        return redirect('cart')

# Update Cart Item
@login_required
def update_cart_item(request, item_id):
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))  # Ensure quantity is an integer
        cart_item = get_object_or_404(CartItem, id=item_id)
        
        if quantity <= 0:
            messages.error(request, "Quantity must be a positive number.")
            return redirect('cart')  # Redirect back to the cart if quantity is invalid

        cart_item.quantity = quantity
        cart_item.save()
        messages.success(request, "Cart item updated successfully.")
        return redirect('cart')  # Redirect back to the cart
    
    
    
    
    


    
# @login_required
# def checkout(request):
#     try:
#         cart = Cart.objects.get(user=request.user)  # Fetch the user's cart
#     except Cart.DoesNotExist:
#         messages.error(request, "Your cart is empty.")
#         return redirect('home')  # Redirect to the home page if cart doesn't exist

#     cart_items = cart.cart_items.all()  # Fetch cart items
#     total_price = sum(item.product.price * item.quantity for item in cart_items)  # Calculate total price

#     if request.method == 'POST':
#         form = CheckoutForm(request.POST)
#         if form.is_valid():
#             order = form.save(commit=False)
#             order.user = request.user
#             order.total_price = total_price  # Set total price for the order
#             order.save()

#             # Create Order Items
#             for item in cart_items:
#                 OrderItem.objects.create(
#                     order=order,
#                     product=item.product,
#                     quantity=item.quantity,
#                     price=item.product.price  # Just use unit price
#                 )

#             # Clear the cart
#             cart.cart_items.all().delete()

#             messages.success(request, "Your order has been placed successfully!")
#             return redirect('order_confirmation', order_id=order.id)
#     else:
#         form = CheckoutForm()

#     return render(request, 'checkout.html', {
#         'form': form,
#         'cart_items': cart_items,
#         'total_price': total_price,  # Pass the calculated total price
#     })
    
    







# Razorpay client setup (replace with your actual Razorpay key and secret)
# client = razorpay.Client(auth=("rzp_test_0FFivWycLQyU7t", "bIVZ4NPOyl9nlyNkoRUwdYDM"))

@login_required
def checkout(request):
    try:
        cart = Cart.objects.get(user=request.user)  # Fetch the user's cart
    except Cart.DoesNotExist:
        messages.error(request, "Your cart is empty.")
        return redirect('home')

    cart_items = cart.cart_items.all()  # Fetch cart items
    total_price = sum(item.product.price * item.quantity for item in cart_items)  # Calculate total price

    # Round the total price for display but keep original for calculations
    total_price_rounded = int(total_price)

    # Ensure the total price is multiplied by 100 to convert it to paise for Razorpay
    amount_in_paise = int(total_price * 100)

    # Initialize Razorpay client
    razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

    try:
        # Create a Razorpay order
        razorpay_order = razorpay_client.order.create({
            "amount": amount_in_paise,  # Amount in paise
            "currency": "INR",
            "payment_capture": "1"
        })
    except Exception as e:
        messages.error(request, "There was an issue creating the Razorpay order. Please try again.")
        return redirect('cart')

    context = {
        'razorpay_key': settings.RAZORPAY_KEY_ID,  # Razorpay public key from settings
        'razorpay_order_id': razorpay_order['id'],  # Razorpay order ID
        'total_price': total_price_rounded,  # Rounded total price for display
        'cart_items': cart_items  # Pass cart items to the template
    }

    return render(request, 'checkout.html', context)


# @login_required
# def checkout(request):
#     try:
#         cart = Cart.objects.get(user=request.user)  
#     except Cart.DoesNotExist:
#         messages.error(request, "Your cart is empty.")
#         return redirect('home')

#     cart_items = cart.cart_items.all()
#     total_price = sum(item.product.price * item.quantity for item in cart_items)

#     # Round the total price to an integer for display
#     total_price_rounded = int(total_price)

#     amount = float(total_price * 100)

#     razorpay_order = razorpay_client.order.create({
#         "amount": amount,
#         "currency": "INR",
#         "payment_capture": "1"
#     })

#     context = {
#         'razorpay_key': settings.RAZORPAY_KEY_ID,
#         'razorpay_order_id': razorpay_order['id'],
#         'total_price': total_price_rounded,  # Pass the rounded total price
#         'cart_items': cart_items
#     }

#     return render(request, 'checkout.html', context)

@login_required
def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'order_confirmation.html', {'order': order})







logger = logging.getLogger("home.apps.HomeConfig")

@csrf_exempt
@login_required
def payment_success(request):
    print("SUCCESS VIEWS START HERE")
    if request.method == 'POST':
        # Debug: Log when the payment success view is hit
        print("Payment success view hit")

        # Get payment details
        payment_id = request.POST.get('razorpay_payment_id')
        razorpay_order_id = request.POST.get('razorpay_order_id')
        signature = request.POST.get('razorpay_signature')

        # Debug: Log received payment details
        print("Received payment ID:", payment_id)
        print("Received order ID:", razorpay_order_id)
        print("Received signature:", signature)

        # Fetch cart items
        cart = Cart.objects.get(user=request.user)
        items = cart.cart_items.all()

        if not items:
            return JsonResponse({'status': 'failed', 'message': 'Cart is empty'}, status=400)

        total_price = sum(item.product.price * item.quantity for item in items)

        # Create Order
        order = Order.objects.create(
            user=request.user,
            name=request.POST.get('name'),
            email=request.POST.get('email'),
            address=request.POST.get('address'),
            phone=request.POST.get('phone'),
            payment_method='razorpay',
            total_price=total_price,
            status='Pending'
        )

        # Create Order Items
        for item in items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )

        # Clear cart
        cart.cart_items.all().delete()

        # Debug: Log order details
        print("Order created successfully:")
        print("Order ID:", order.id)
        print("User:", order.user.username)
        print("Total Price:", order.total_price)
        print("Items:")
        for item in order.items.all():  # Accessing related order items
            print(f" - {item.product.name} x {item.quantity} at ₹{item.price}")

        return JsonResponse({'status': 'success', 'payment_id': payment_id, 'order_id': order.id})

    return JsonResponse({'status': 'failed'}, status=400)



@login_required
def order_management_dashboard(request):
    # Fetch all orders (or filter based on user, date, etc.)
    orders = Order.objects.all()  # Adjust based on your logic

    # Check if orders exist by printing in the console
    print(orders)  # To see if orders are being fetched

    return render(request, 'order_management_dashboard.html', {'orders': orders})




def change_order_status(request, order_id):
    if request.method == 'POST':
        order = get_object_or_404(Order, id=order_id)
        new_status = request.POST.get('status')

        # logger.info(f'Changing status for Order ID {order_id} to {new_status}')

        if new_status:
            order.status = new_status
            order.save()
            messages.success(request, f'Status updated to {new_status} for Order ID {order.id}.')
        else:
            messages.error(request, 'Invalid status.')

    return redirect('order_management_dashboard')

def delete_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order.delete()
    return redirect('order_management_dashboard')