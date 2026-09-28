import django_filters
from .models import Product


class ProductFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    category = django_filters.CharFilter(field_name='category__slug', lookup_expr='exact')
    # ^ TZ misolida "?category=elektronika" — bu SLUG bo'yicha filtrlash,
    # ID bo'yicha emas, chunki foydalanuvchi uchun "elektronika" o'qilishi
    # osonroq, raqamli ID'ni bilmaydi

    class Meta:
        model = Product
        fields = ['category', 'min_price', 'max_price']