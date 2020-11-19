from decimal import Decimal
from django.conf import settings
from onlinestore.models import Product


class Cart:

    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product: Product, quantity=1, override_quantity=True):
        """
        Add a product to the cart.
        """
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0,
                                     'price': str(product.price)}
        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def remove(self, product: Product):
        """
        Remove a product from the cart.
        """
        product_id = str(product.id)
        if product_id in self.cart:
            del(self.cart[product_id])
            self.save()

    def get_total_quantity(self):
        """
        Count the quantity of all items in the cart.
        """
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        """
        Count total price of all items in the cart.
        """
        return sum(
            Decimal(item['price']) * item['quantity']
            for item in self.cart.values()
        )

    def __iter__(self):
        """
        Iterate over items in the cart and get the products
        from the database.
        """
        for product_id in self.cart:
            product = Product.objects.get(id=product_id)
            item = self.cart[product_id]
            price = Decimal(item['price'])
            total_price = price * item['quantity']

            returning_item = dict(
                item,
                product=product,
                price=price,
                total_price=total_price
            )

            yield returning_item

    def clear(self):
        """
        Remove cart from a session
        """
        del(self.session[settings.CART_SESSION_ID])
        self.save()

    def save(self):
        """
        Save the session
        """
        self.session.modified = True
