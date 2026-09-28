from django.db import models
from base.models import BaseModel


class Category(BaseModel):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    parent = models.ForeignKey(
        'self', null=True, blank=True,
        on_delete=models.SET_NULL, related_name='subcategories'
    )

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Product(BaseModel):
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name='products'
    )
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='products/', blank=True, null=True)

    def __str__(self):
        return self.name