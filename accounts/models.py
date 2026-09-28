from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('customer', 'Mijoz'),
    )
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)
    adress = models.CharField(max_length=120)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='customer')

    def __str__(self):
        return f"{self.username} ({self.role})"