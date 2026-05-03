from django.urls import path
from . import views


app_name = 'listings'

urlpatterns = [
    path("dashboard/", views.dashboard, name="dashboard"),
    path("add/", views.add_product, name="add_product"),
    path("product/<int:pk>/", views.product_detail, name="product_detail"),
    path("delete/<int:pk>/", views.delete_product, name="delete_product"),
    path("buy/<int:pk>/", views.buy_product, name="buy_product"),
]