from django.test import TestCase
from django.urls import reverse
from onlinestore.models import Product, Category


def create_products(count):
    '''
    Create a given number of products
    '''
    category = Category(name='Test category',
                        slug='test-category',
                        image='/static/onlinestore/images/no-product-image.png')
    category.save()
    products = []
    for i in range(count):
        product = Product.objects.create(name=f'Product №{i + 1}',
                                         price=100,
                                         slug=f'product-{i + 1}',
                                         popularity=(i / 10),
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

    def test_popular_products_all_showed(self):
        create_products(8)
        response = self.client.get(reverse('onlinestore:main'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['popular_products'],
                                 ['<Product: Product №1>',
                                  '<Product: Product №2>',
                                  '<Product: Product №3>',
                                  '<Product: Product №4>',
                                  '<Product: Product №5>',
                                  '<Product: Product №6>',
                                  '<Product: Product №7>',
                                  '<Product: Product №8>'],
                                 ordered=False)

    def test_popular_products_only_eight_max_popular_showed(self):
        create_products(16)
        response = self.client.get(reverse('onlinestore:main'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['popular_products'],
                                 ['<Product: Product №9>',
                                  '<Product: Product №10>',
                                  '<Product: Product №11>',
                                  '<Product: Product №12>',
                                  '<Product: Product №13>',
                                  '<Product: Product №14>',
                                  '<Product: Product №15>',
                                  '<Product: Product №16>'],
                                 ordered=False)

    def test_sale_without_discount_only(self):
        create_products(4)
        response = self.client.get(reverse('onlinestore:main'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['sale_item'], None)

    def test_sale_only_one_product_with_discount(self):
        products = create_products(4)
        product_with_discount = products[0]
        product_with_discount.sale = True
        product_with_discount.discount_price = 1
        product_with_discount.save()
        response = self.client.get(reverse('onlinestore:main'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['sale_item'],
                         product_with_discount)
