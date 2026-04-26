from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    email = models.EmailField(unique=True, db_index=True)
    password = models.CharField(max_length=128)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "password"]

    def __str__(self):
        return self.email
    

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    bio = models.TextField()
    location = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    image = models.ImageField(upload_to="profile_images/", null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    likes = models.ManyToManyField(User, related_name="liked_profiles", blank=True)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"    
