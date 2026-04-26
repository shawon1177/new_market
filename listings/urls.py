from django.urls import path
from .views import food_list, create_food

urlpatterns = [
    path('', food_list, name='food_list'),
    path('create/', create_food, name='create_food'),
]