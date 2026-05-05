from django.urls import path
from . import views


app_name = 'listings'

urlpatterns = [
    path("dashboard/", views.dashboard, name="dashboard"),
    path("add/", views.add_product, name="add_product"),
    path("product/<int:pk>/", views.product_detail, name="product_detail"),
    path("delete/<int:pk>/", views.delete_product, name="delete_product"),
    path("buy/<int:pk>/", views.buy_product, name="buy_product"),
    path("cart/", views.cart_view, name="cart"),
    path("cart/add/<int:pk>/", views.add_to_cart, name="add_to_cart"),
    path("cart/remove/<int:pk>/", views.remove_from_cart, name="remove_from_cart"),
    path("cart/place-order/", views.place_order_cart, name="place_order_cart"),
    path("cart/update/<int:pk>/<str:action>/", views.update_cart, name="update_cart"),
    path("order/<int:pk>/", views.order_detail, name="order_detail"),

]