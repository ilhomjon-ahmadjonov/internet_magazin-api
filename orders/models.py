from django.db import models
from base.models import BaseModel
from accounts.models import CustomUser
from products.models import Product


class Cart(BaseModel):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='cart')

    def __str__(self):
        return f"{self.user.username} - Savatchasi"


class CartItem(BaseModel):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    count = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('cart', 'product')

    def __str__(self):
        return f"{self.card.user.username} -> {self.product}"


class Order(BaseModel):
    STATUS_CHOICES = (
        ('pending', 'Kutilmoqda'),
        ('shipping', 'Yetkazilmoqda'),
        ('completed', 'Bajarildi'),
        ('cancelled', 'Bekor qilindi'),
    )
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='orders')
    address = models.CharField(max_length=120)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    @property
    def total_price(self):
        return sum(item.price for item in self.items.select_related('product').all())

    def __str__(self):
        return f"Order #{self.id} - {self.user.username}"


class OrderItem(BaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name='product_orders')
    count = models.PositiveIntegerField(default=1)
    price_at_purchase = models.DecimalField(max_digits=10, decimal_places=2)


    @property
    def price(self):
        return self.count * self.price_at_purchase

    def __str__(self):
        return f"{self.order.id} -> {self.product}"