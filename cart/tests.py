from django.test import TestCase
from django.conf import settings
from onlinestore.models import Product, Category
from .cart import Cart, ProductNotAvailableException
from decimal import Decimal


class CartTestCase(TestCase):

    def setUp(self):
        self.cart_session_id = settings.CART_SESSION_ID
        self.category = Category.objects.create(name='test category',
                                                slug='test-category')
        self.product = Product.objects.create(name='Test product',
                                              price=100,
                                              slug='test-product',
                                              category=self.category)
        self.product_2 = Product.objects.create(name='Test product №2',
                                                price=350,
                                                slug='test-product-2',
                                                category=self.category)
        self.session = self.client.session
        self.session.save()
        self.cart = Cart(self.session)

    def test_new_cart_is_empty(self):
        self.assertEqual(0, self.cart.get_total_quantity())

    def test_cart_add_product(self):
        self.cart.add(self.product)
        self.assertDictEqual(
            self.session[self.cart_session_id][str(self.product.id)],
            {'quantity': 1, 'price': '100'}
        )
        self.assertEqual(1, self.cart.get_total_quantity())
        self.assertTrue(self.cart.contains(self.product))

    def test_cart_add_product_twice(self):
        self.cart.add(self.product)
        self.cart.add(self.product)
        self.assertDictEqual(
            self.session[self.cart_session_id][str(self.product.id)],
            {'quantity': 1, 'price': '100'}
        )
        self.assertEqual(1, self.cart.get_total_quantity())
        self.assertTrue(self.cart.contains(self.product))

    def test_cart_update_product_quantity(self):
        self.cart.add(self.product)
        self.cart.update(self.product, 3)
        self.assertDictEqual(
            self.session[self.cart_session_id][str(self.product.id)],
            {'quantity': 3, 'price': '100'}
        )
        self.assertEqual(3, self.cart.get_total_quantity())
        self.assertTrue(self.cart.contains(self.product))

    def test_add_two_products_and_update_quanity(self):
        self.cart.add(self.product)
        self.cart.add(self.product_2)
        self.cart.update(self.product, 3)
        self.cart.update(self.product_2, 4)
        self.assertDictEqual(
            self.session[self.cart_session_id][str(self.product.id)],
            {'quantity': 3, 'price': '100'}
        )
        self.assertDictEqual(
            self.session[self.cart_session_id][str(self.product_2.id)],
            {'quantity': 4, 'price': '350'}
        )
        self.assertTrue(self.cart.contains(self.product))
        self.assertTrue(self.cart.contains(self.product_2))
        self.assertEqual(7, self.cart.get_total_quantity())

    def test_try_to_add_unavailable_product_to_cart(self):
        self.product.available = False
        self.product.save()

        self.assertRaises(ProductNotAvailableException,
                          self.cart.add, self.product)

    def test_get_total_price_with_empty_cart(self):
        self.assertEqual(0, self.cart.get_total_price())

    def test_get_total_price_with_one_product(self):
        self.cart.add(self.product)
        self.assertEqual(100, self.cart.get_total_price())

    def test_get_total_price_with_two_products_and_changed_quantity(self):
        self.cart.add(self.product)
        self.cart.add(self.product_2)
        self.cart.update(self.product, 2)
        self.cart.update(self.product_2, 3)
        self.assertEqual(2 * 100 + 3 * 350, self.cart.get_total_price())

    def test_cart_remove(self):
        self.cart.add(self.product)
        self.cart.remove(self.product)
        self.assertEqual(0, self.cart.get_total_quantity())
        self.assertFalse(self.cart.contains(self.product))

    def test_remove_from_empty_cart(self):
        self.cart.remove(self.product)
        self.assertEqual(0, self.cart.get_total_quantity())

    def test_iteration(self):
        self.cart.add(self.product)
        self.cart.add(self.product_2)
        self.cart.update(self.product, 3)
        self.cart.update(self.product_2, 4)
        self.assertCountEqual(
            first=[{'product': self.product,
                    'price': Decimal(100),
                    'quantity': 3,
                    'total_price': Decimal(300)},
                   {'product': self.product_2,
                    'price': Decimal(350),
                    'quantity': 4,
                    'total_price': Decimal(1400)}],
            second=[item for item in self.cart]
        )

    def test_product_with_discount(self):
        self.product.sale = True
        self.product.discount_price = 80
        self.product.save()
        self.cart.add(self.product)
        self.cart.update(self.product, 2)
        self.assertEqual(
            first=[{'product': self.product,
                    'price': Decimal(80),
                    'quantity': 2,
                    'total_price': Decimal(160)}],
            second=[item for item in self.cart]
        )
