from decimal import Decimal
from products.models import Product

class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart')
        if not cart:
            cart = self.session['cart'] = {}
        self.cart = cart

    def add(self, product, quantity=1):
        product_id = str(product.id)
        if product_id not in self.cart:
            # Debugging the price before adding to the cart
            print(f"Adding product {product_id} with price: {product.price}")
            self.cart[product_id] = {
                'quantity': 0,
                'price': str(product.price)  # Ensure it's stored as a string
        }
        self.cart[product_id]['quantity'] += quantity
        self.save()
    
    def save(self):
        # Mark the session as modified to save changes
        self.session.modified = True

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def clear(self):
        del self.session['cart']
        self.save()

    def get_total_price(self):
        # Convert price back to Decimal for calculations
        total_price = sum(
            Decimal(item['price']) * item['quantity'] for item in self.cart.values()
        )
        return total_price

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        for product in products:
            cart_item = self.cart[str(product.id)]
            # Convert price back to Decimal for accuracy
            cart_item['price'] = Decimal(cart_item['price'])
            cart_item['product'] = product
            cart_item['total_price'] = cart_item['price'] * cart_item['quantity']
            yield cart_item
