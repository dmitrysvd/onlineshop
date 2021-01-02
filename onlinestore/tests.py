from django.test import TestCase
from django.urls import reverse
from onlinestore.models import Brand, Product, Category


def create_products(count, category=None):
    '''
    Create a given number of products
    '''
    if not category:
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


class CategoryModelsTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='test category',
                                                slug='test-category',
                                                image='test-image')

    def test_category_fields(self):
        self.assertEqual(self.category.name, 'test category')
        self.assertEqual(self.category.slug, 'test-category')
        self.assertEqual(self.category.image, 'test-image')


class ProductModelTests(TestCase):

    def setUp(self):
        self.category = Category.objects.create(name='test category',
                                                slug='test-category')
        self.product = Product.objects.create(name='Test product',
                                              price=100,
                                              slug='test-product',
                                              popularity=0.1,
                                              category=self.category,
                                              model_name='test',
                                              engine_power=100,
                                              engine_type='gas',
                                              number_of_seats=1,
                                              year_of_issue=2017)

    def test_binded_category(self):
        self.assertEqual(self.product.category.name, 'test category')

    def test_product_properties(self):
        self.assertEqual(self.product.name, 'Test product')
        self.assertEqual(self.product.price, 100)
        self.assertEqual(self.product.slug, 'test-product')
        self.assertEqual(self.product.popularity, 0.1)
        self.assertEqual(self.product.category, self.category)
        self.assertEqual(self.product.model_name, 'test')
        self.assertEqual(self.product.engine_power, 100)
        self.assertEqual(self.product.engine_type, 'gas')
        self.assertEqual(self.product.number_of_seats, 1)
        self.assertEqual(self.product.year_of_issue, 2017)

    def test_current_price_not_no_discount(self):
        self.product.price = 1000
        self.product.save()
        self.assertEqual(self.product.current_price, 1000)

    def test_current_price_discount_defined_but_sale_is_false(self):
        self.product.price = 1000
        self.product.discount_price = 800
        self.product.sale = False
        self.product.save()
        self.assertEqual(self.product.current_price, 1000)

    def test_current_price_discount_defined_and_sale_is_true(self):
        self.product.price = 1000
        self.product.discount_price = 800
        self.product.sale = True
        self.product.save()
        self.assertEqual(self.product.current_price, 800)


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


class BrandModelTests(TestCase):

    def test_brand_fields(self):
        brand = Brand.objects.create(name='my brand')
        self.assertEqual(brand.name, 'my brand')


class ProductListViewTests(TestCase):

    def setUp(self):
        self.max_products_per_page = 12
        self.category = Category.objects.create(name='test_category',
                                                slug='test-category')

    def test_no_products(self):
        response = self.client.get(self.category.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'test_category')
        self.assertContains(response, 'не найдено')

    def test_products_amount_eq_max(self):
        products = create_products(count=self.max_products_per_page,
                                   category=self.category)
        response = self.client.get(self.category.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        page_obj = response.context['page_obj']
        self.assertQuerysetEqual(page_obj.object_list,
                                 [
                                     '<Product: Product №1>',
                                     '<Product: Product №2>',
                                     '<Product: Product №3>',
                                     '<Product: Product №4>',
                                     '<Product: Product №5>',
                                     '<Product: Product №6>',
                                     '<Product: Product №7>',
                                     '<Product: Product №8>',
                                     '<Product: Product №9>',
                                     '<Product: Product №10>',
                                     '<Product: Product №11>',
                                     '<Product: Product №12>',
                                 ],
                                 ordered=False)
        self.assertEqual(page_obj.paginator.num_pages, 1)

    def test_products_amount_more_than_max_per_page(self):
        products = create_products(count=self.max_products_per_page + 1,
                                   category=self.category)
        response = self.client.get(self.category.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        page_obj = response.context['page_obj']
        self.assertQuerysetEqual(page_obj.object_list,
                                 [
                                     '<Product: Product №13>',
                                     '<Product: Product №12>',
                                     '<Product: Product №11>',
                                     '<Product: Product №10>',
                                     '<Product: Product №9>',
                                     '<Product: Product №8>',
                                     '<Product: Product №7>',
                                     '<Product: Product №6>',
                                     '<Product: Product №5>',
                                     '<Product: Product №4>',
                                     '<Product: Product №3>',
                                     '<Product: Product №2>',
                                 ],
                                 ordered=False)
        self.assertEqual(page_obj.number, 1)
        self.assertEqual(page_obj.paginator.num_pages, 2)


class ProductDetailViewTests(TestCase):

    def setUp(self):
        self.category = Category.objects.create(name='Test category',
                                                slug='test-category')
        self.brand = Brand.objects.create(name='My brand')
        self.product = Product.objects.create(name='Test product',
                                              price=102700,
                                              slug='test-product',
                                              category=self.category,
                                              brand=self.brand,
                                              model_name='Model name',
                                              engine_power=113,
                                              engine_type='gas',
                                              number_of_seats=132,
                                              year_of_issue=2017)

    def test_try_to_open_not_existing_product(self):
        response = self.client.get(reverse('onlinestore:product_detail',
                                           args=[3]))
        self.assertEqual(response.status_code, 404)

    def test_open_existing_product_without_discount(self):
        response = self.client.get(reverse('onlinestore:product_detail',
                                           args=[self.product.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test product')
        self.assertContains(response, '102700')
        self.assertContains(response, self.category.name)
        self.assertContains(response, 'My brand')
        self.assertContains(response, 'Model name')
        self.assertContains(response, '113')
        self.assertContains(response, 'Бензиновый')
        self.assertContains(response, '132')
        self.assertContains(response, '2017')

    def test_open_existing_product_with_discount(self):
        self.product.discount_price = 99415
        self.product.sale = True
        self.product.save()
        response = self.client.get(reverse('onlinestore:product_detail',
                                           args=[self.product.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test product')
        self.assertContains(response, '102700')
        self.assertContains(response, '99415')
        self.assertContains(response, self.category.name)
        self.assertContains(response, 'My brand')
        self.assertContains(response, 'Model name')
        self.assertContains(response, '113')
        self.assertContains(response, 'Бензиновый')
        self.assertContains(response, '132')
        self.assertContains(response, '2017')
