from django.contrib import admin
from django.urls import path, include
from home import views
from django.conf import settings
from django.conf.urls.static import static
from .views import (
    home, loginuser, registration, product_list,
    order_product, view_cart, add_to_cart, update_cart_item,Order,OrderItem
)



urlpatterns = [
    path("home/", views.home, name="home"),
    # path('home/', views.home, name='home'), 
    path("login/", views.loginuser, name="login"),
    path("registration/", views.registration, name="registration"),
    path("products/", views.product_list, name="product_list"),
    path("order/<int:id>/", views.order_product, name="order_product"),
    path("our_story/", views.our_story, name="our_story"),
    path("chef_special/", views.chef_special, name="chef_special"),
    path("catering/", views.catering, name="catering"),
    path("profile/", views.profile_view, name="profile"),
    path("cart/", view_cart, name="cart"),  # Ensure this matches your view
    path("add-to-cart/", add_to_cart, name="add_to_cart"),
    path("update-cart-item/<int:item_id>/", update_cart_item, name="update_cart_item"),
  
    path('order-confirmation/<int:order_id>/', views.order_confirmation, name='order_confirmation'),
    path("checkout/", views.checkout, name="checkout"),
    path('payment-success/', views.payment_success, name='payment_success'),

    # path('payment-failed/', views.payment_failed, name='payment_failed'),
    path('dashboard/orders/', views.order_management_dashboard, name='order_management_dashboard'),
    path('dashboard/orders/change-status/<int:order_id>/', views.change_order_status, name='change_order_status'),
    path('dashboard/orders/delete/<int:order_id>/', views.delete_order, name='delete_order'),  # New URL for deleting an order


    
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
