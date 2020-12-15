from django.conf import settings
from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    image = models.ImageField(blank=True,
                              upload_to='images/categories/')

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("onlinestore:product_list", args=[self.slug])


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

    def save(self, *args, **kwargs):
        if self.discount_price is None:
            self.sale = False
        super().save(*args, **kwargs)

    def current_price(self):
        return self.discount_price if self.sale else self.price

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("onlinestore:product_detail", args=[self.pk])
