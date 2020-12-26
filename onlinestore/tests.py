from django.test import TestCase
from django.urls import reverse
from onlinestore.models import ENGINE_TYPE_CHOICES, Product, Category


def create_products(count):
    '''
    Create a given number of products
    '''
    category = Category(name='Test category')
    category.save()
    products = []
    for i in range(count):
        product = Product.objects.create(name=f'Product №{i + 1}',
                                         price=100,
                                         slug=f'product-{i + 1}',
                                         category=category,
                                         model_name='test',
                                         engine_power=100,
                                         engine_type='gas',
                                         number_of_seats=1,
                                         year_of_issue=2017)
        product.save()
        products.append(product)
    return products


class ProductModelTests(TestCase):

    def setUp(self):
        self.category = Category()
        self.category.save()

    def test_current_price_not_no_discount(self):
        product = Product(price=1000)
        self.assertEqual(product.current_price, 1000)

    def test_current_price_discount_defined_but_sale_is_false(self):
        product = Product(price=1000, discount_price=800, sale=False)
        self.assertEqual(product.current_price, 1000)

    def test_current_price_discount_defined_and_sale_is_true(self):
        product = Product(price=1000, discount_price=800, sale=True)
        self.assertEqual(product.current_price, 800)


class MainViewTests(TestCase):

    def test_no_products(self):
        response = self.client.get(reverse('onlinestore:main'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['popular_products'], [])
        self.assertEqual(response.context['sale_item'], None)
