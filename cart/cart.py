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

    def add(self, product: Product):
        """
        Add product to cart.
        """
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 1,
                                     'price': str(product.current_price)}
        self.save()

    def update(self, product: Product, quantity: int):
        """
        Update product quantity.
        """
        product_id = str(product.id)
        if product_id not in self.cart:
            self.add(product)
        self.cart[product_id]['quantity'] = quantity
        self.save()

    def remove(self, product: Product):
        """
        Remove product from cart.
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

    def contains(self, product: Product):
        return str(product.id) in self.cart.keys()

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
