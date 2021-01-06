from django import template

register = template.Library()


@register.inclusion_tag('onlinestore/product_item.html')
def product_item(product):
    return {'product': product}
