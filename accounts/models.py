from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    email = models.EmailField(unique=True, db_index=True)
    phone = models.CharField(max_length=20, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.email
    

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    bio = models.TextField()
    location = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.user.username}'s Profile"    
