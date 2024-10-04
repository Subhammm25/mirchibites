from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from decimal import Decimal
import razorpay
from .models import Product, UserProfile, Cart, CartItem, Order, OrderItem
from .forms import RegistrationForm, CheckoutForm
from django.utils import timezone
import pytz


# Razorpay client setup
razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

# Home View
def home(request):
    return render(request, "home.html")

# Login View
def loginuser(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
        else:
            if not User.objects.filter(username=username).exists():
                messages.error(request, "No account found with this username.")
            else:
                messages.error(request, "Invalid username or password.")
    return render(request, 'login.html')

# Registration View
def registration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            phone_number = form.cleaned_data.get('phone_number')

            # Check if username or email already exists
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username is already taken. Please choose another one.')
            elif User.objects.filter(email=email).exists():
                messages.error(request, 'An account with this email already exists.')
            else:
                # Save the user but mark as active, as you're not using OTP or email verification
                user = form.save(commit=False)
                user.is_active = True  # Set active to True as you aren't doing verification
                user.save()

                # Log the user in after registration
                login(request, user)
                
                # Success message
                messages.success(request, 'Registration successful! You are now logged in.')

                # Redirect to home page after successful registration
                return redirect('home')  # Replace 'home' with your homepage's URL pattern name
        else:
            # Handle form validation errors
            for field, error in form.errors.items():
                error_message = f"{field}: {error[0]}"
                messages.error(request, error_message)

    else:
        form = RegistrationForm()

    return render(request, 'registration.html', {'form': form})



# Product List View
def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})

# Order Product View
def order_product(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, 'order_product.html', {'product': product})

# Static Pages Views
def our_story(request):
    return render(request, "our_story.html")

def chef_special(request):
    return render(request, "chef_special.html")

def catering(request):
    return render(request, "catering.html")

# User Profile View
@login_required
def profile_view(request):
    user = request.user
    try:
        user_profile = UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        user_profile = UserProfile.objects.create(user=user)

    past_orders = Order.objects.filter(user=user).order_by('-created_at')
    
    context = {
        'user_profile': user_profile,
        'past_orders': past_orders
    }
    return render(request, 'profile.html', context)


# Cart Views
@login_required
def view_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.cart_items.all()
    return render(request, 'cart.html', {'cart_items': cart_items})

@login_required
def add_to_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity', 1))

        product = get_object_or_404(Product, id=product_id)
        cart, created = Cart.objects.get_or_create(user=request.user)
        
        cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not item_created:
            cart_item.quantity += quantity
        else:
            cart_item.quantity = quantity
        cart_item.save()

        return redirect('cart')

@login_required
def update_cart_item(request, item_id):
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        cart_item = get_object_or_404(CartItem, id=item_id)
        
        if quantity <= 0:
            messages.error(request, "Quantity must be a positive number.")
        else:
            cart_item.quantity = quantity
            cart_item.save()
            messages.success(request, "Cart item updated successfully.")
        
        return redirect('view_cart')


from django.utils import timezone
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from home.models import Cart, Order, OrderItem
import razorpay
from django.conf import settings

razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

@login_required
def checkout(request):
    print("viewing")
    try:
        cart = Cart.objects.get(user=request.user)
    except Cart.DoesNotExist:
        messages.error(request, "Your cart is empty.")
        return redirect('home')

    cart_items = cart.cart_items.all()
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    total_price_rounded = int(total_price)
    amount_in_paise = int(total_price * 100)

    if request.method == "POST":
        # Ensure form fields are available and valid
        name = request.POST.get('name')
        email = request.POST.get('email')
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        payment_method = request.POST.get('payment_method', 'COD')  # Default to COD

        if name and email and address and phone:
            # Create the order
            order = Order.objects.create(
                user=request.user,
                name=name,
                email=email,
                address=address,
                phone=phone,
                payment_method=payment_method,
                total_price=total_price_rounded,
                created_at=timezone.now(),
                status='Pending'
            )
            print(f"Order created: {order.id}")

            # Create order items
            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.price
                )
            print("Order items created")

            # Clear the cart after order creation
            cart.cart_items.all().delete()
            cart.delete()

            # Redirect to order confirmation or success page
            return redirect('order_confirmation', order_id=order.id)
        else:
            # If form data is missing
            messages.error(request, "Please fill in all the required details.")

    razorpay_order = razorpay_client.order.create({
        "amount": amount_in_paise,
        "currency": "INR",
        "payment_capture": "1"
    })

    context = {
        'razorpay_key': settings.RAZORPAY_KEY_ID,
        'razorpay_order_id': razorpay_order['id'],
        'total_price': total_price_rounded,
        'cart_items': cart_items
    }

    return render(request, 'checkout.html', context)


import logging

# Payment Success View

# Setup logging
logger = logging.getLogger("home")


@csrf_exempt
@login_required
def payment_success(request):
    if request.method == 'POST':
        logger.info("Payment success view called.")

        payment_id = request.POST.get('razorpay_payment_id')
        razorpay_order_id = request.POST.get('razorpay_order_id')
        signature = request.POST.get('razorpay_signature')

        # Check if the cart exists for the user
        try:
            cart = Cart.objects.get(user=request.user)
            logger.info(f"Cart retrieved for user: {request.user.username}.")
        except Cart.DoesNotExist:
            logger.error("Cart does not exist.")
            return JsonResponse({'status': 'failed', 'message': 'Cart does not exist'}, status=400)

        # Get the cart items
        items = cart.cart_items.all()

        # Check if the cart has items
        if not items:
            logger.error("No items in cart.")
            return JsonResponse({'status': 'failed', 'message': 'No items in cart'}, status=400)

        # Calculate total price
        total_price = sum(item.product.price * item.quantity for item in items)
        logger.info(f"Total price calculated: {total_price}")

        # Create the order
        try:
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
            print(f"Name: {name}, Email: {email}, Address: {address}, Phone: {phone}, Payment Method: {payment_method}")
            logger.info(f"Order created successfully: Order ID {order.id}.")
        except Exception as e:
            logger.error(f"Order creation failed: {str(e)}")
            return JsonResponse({'status': 'failed', 'message': f'Order creation failed: {str(e)}'}, status=400)

        # Create order items
        for item in items:
            try:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.price
                )
                logger.info(f"Order item created: Product ID {item.product.id}, Quantity {item.quantity}.")
            except Exception as e:
                logger.error(f"Order item creation failed: {str(e)}")
                return JsonResponse({'status': 'failed', 'message': f'Order item creation failed: {str(e)}'}, status=400)

        # Clear the cart
        cart.cart_items.all().delete()
        logger.info("Cart items cleared after order creation.")

        return JsonResponse({'status': 'success', 'payment_id': payment_id, 'order_id': order.id})

    return JsonResponse({'status': 'failed'}, status=400)




@login_required
def order_confirmation(request, order_id):
    # Get the order by ID for the logged-in user
    try:
        order = Order.objects.get(id=order_id, user=request.user)
    except Order.DoesNotExist:
        messages.error(request, "Order not found.")
        return redirect('home')  # Redirect to homepage if the order is not found

    # Get all the items related to the order using the reverse relation with the custom related name 'items'
    order_items = order.items.all()

    # Render the confirmation page with the order and order items
    context = {
        'order': order,
        'order_items': order_items,
    }
    return render(request, 'order_confirmation.html', context)



# Order Management Dashboard
@login_required
def order_management_dashboard(request):
    orders = Order.objects.all()
    return render(request, 'order_management_dashboard.html', {'orders': orders})

# Change Order Status
@login_required
def change_order_status(request, order_id):
    if request.method == 'POST':
        order = get_object_or_404(Order, id=order_id)
        new_status = request.POST.get('status')
        
        if new_status:
            order.status = new_status
            order.save()
            messages.success(request, f'Status updated to {new_status} for Order ID {order.id}.')
        else:
            messages.error(request, 'Invalid status.')

    return redirect('order_management_dashboard')

# Delete Order
@login_required
def delete_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order.delete()
    return redirect('order_management_dashboard')


