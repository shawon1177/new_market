from django.db import models
from django.conf import settings

CATEGORY_CHOICES = [
    ('veg', 'Vegetarian'),
    ('nonveg', 'Non-Vegetarian'),
    ('dessert', 'Dessert'),
    ('beverage', 'Beverage'),
]


class FoodItem(models.Model):
    seller = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='foods',
        db_index=True
    )

    title = models.CharField(max_length=200, db_index=True)
    description = models.TextField()

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        db_index=True
    )

    image = models.ImageField(upload_to='foods/')

    availability_status = models.BooleanField(default=True, db_index=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, db_index=True, default='veg' )
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True, db_index=True)

    class Meta:
        indexes = [
            models.Index(fields=['price']),
            models.Index(fields=['availability_status']),
        ]