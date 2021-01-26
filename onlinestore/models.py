from django.conf import settings
from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    image = models.ImageField(upload_to='images/categories/')

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("onlinestore:product_list", args=[self.slug])


class Brand(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


ENGINE_TYPE_CHOICES = (
    ('gas', 'Бензиновый'),
    ('electric', 'Электрический'),
    ('diesel', 'Дизельный'),
)

COUNTRY_CHOICES = (
    ('canada', 'Канада'),
    ('usa', 'Америка'),
    ('russia', 'Россия'),
    ('china', 'Китай')
)


class AvailableProductsManager(models.Manager):
    def get_queryset(self):
        return super(AvailableProductsManager, self).get_queryset() \
                                                    .filter(available=True)


class Product(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    image = models.ImageField(blank=True,
                              upload_to='images/products/')
    category = models.ForeignKey(Category,
                                 on_delete=models.PROTECT,
                                 related_name='products')
    price = models.DecimalField(max_digits=9, decimal_places=2)
    discount_price = models.DecimalField(max_digits=9,
                                         decimal_places=2,
                                         blank=True, null=True)
    sale = models.BooleanField(default=False)
    description = models.TextField(blank=True)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    popularity = models.FloatField(default=0)

    # product properties
    manufacturer_country = models.CharField(max_length=10,
                                            choices=COUNTRY_CHOICES)
    brand = models.ForeignKey(Brand,
                              on_delete=models.CASCADE,
                              related_name='products',
                              blank=True,
                              null=True)
    model_name = models.CharField(max_length=200)
    engine_power = models.IntegerField()
    engine_type = models.CharField(max_length=10, choices=ENGINE_TYPE_CHOICES)
    number_of_seats = models.IntegerField()
    year_of_issue = models.IntegerField()

    # managers
    objects = models.Manager()
    available_objects = AvailableProductsManager()

    def save(self, *args, **kwargs):
        if self.discount_price is None:
            self.sale = False
        super().save(*args, **kwargs)

    @property
    def current_price(self):
        '''
        Return the current price taking into accout a discount
        '''
        return self.discount_price if self.sale else self.price

    @property
    def discount_percentage(self):
        '''
        Return discount percentage
        '''
        if self.discount_price:
            return 100 - int(100 * self.discount_price / self.price)
        else:
            return 0

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("onlinestore:product_detail", args=[self.pk])
