import django_filters
from .models import COUNTRY_CHOICES, ENGINE_TYPE_CHOICES, Product, Brand


class ProductFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(
        field_name='name', lookup_expr='icontains', label='Название')
    price = django_filters.RangeFilter(field_name='price', label='Цена')
    sale = django_filters.BooleanFilter(field_name='sale', label='Скидка')
    engine_power = django_filters.RangeFilter(
        field_name='engine_power', label='Мощность')
    engine_type = django_filters.MultipleChoiceFilter(
        field_name='engine_type',
        choices=ENGINE_TYPE_CHOICES,
        label='Тип двигателя')
    number_of_seats = django_filters.NumberFilter(
        field_name='number_of_seats', label='Количество мест')
    year_of_issue = django_filters.RangeFilter(
        field_name='year_of_issue', label='Год выпуска')

    manufacturer_country = django_filters.MultipleChoiceFilter(
        field_name='manufacturer_country',
        choices=COUNTRY_CHOICES,
        label='Страна-производитель')
    brand = django_filters.ModelMultipleChoiceFilter(
        field_name='brand', queryset=Brand.objects.all(), label='Марка')

    class Meta:
        model = Product
        fields = []
