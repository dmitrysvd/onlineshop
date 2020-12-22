from django import template
from ..models import Product

register = template.Library()


@register.inclusion_tag('onlinestore/product_slider.html')
def product_slider(products, title=None):
    return {'product_slider_list': products,
            'title': title}
