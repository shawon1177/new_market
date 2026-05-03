from django.db import models
from accounts.models import User
from django.conf import settings

CATEGORY_CHOICES = [
    ('veg', 'Vegetarian'),
    ('nonveg', 'Non-Vegetarian'),
    ('dessert', 'Dessert'),
    ('beverage', 'Beverage'),
]

class Product(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="products"
    )

    title = models.CharField(max_length=200)
    description = models.TextField()

    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)

    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)

    image = models.ImageField(upload_to="products/", null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

    def __str__(self):
        return self.title
    
class Order(models.Model):
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.buyer} bought {self.product.title}"    