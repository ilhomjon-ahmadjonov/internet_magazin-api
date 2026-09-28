from django.db import models
from accounts.models import CustomUser
from django.core.validators import MinValueValidator, MaxValueValidator
from base.models import BaseModel
from products.models import Product


class Like(BaseModel):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE,related_name='likes'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='likes'
    )

    class Meta:
        unique_together = ('user', 'product')

    def __str__(self):
        return f"{self.user.username} -> {self.product.name}"


class Comment(BaseModel):
    user = models.ForeignKey(
        CustomUser,on_delete=models.CASCADE,related_name='comments'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField()
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} ({self.rating}/5) on {self.product.name}"