from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from .models import Product, Order
from django.core.paginator import Paginator
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_control



# 🏠 DASHBOARD = FEED
@never_cache
@login_required
def dashboard(request):
    query = request.GET.get("q")

    # ⚡ FIX: remove N+1 query problem
    products = Product.objects.select_related('owner').only(
        "id", "title", "price", "image", "description", "created_at", "owner__email"
    ).order_by("-id")

    if query:
        products = products.filter(title__icontains=query)


    paginator = Paginator(products, 12)
    page = request.GET.get("page")
    products = paginator.get_page(page)

    return render(request, "listings/dashboard.html", {
        "products": products
    })

# ➕ ADD PRODUCT

@login_required
def add_product(request):
    if request.method == "POST":

        Product.objects.create(
            owner=request.user,
            title=request.POST.get("title"),
            description=request.POST.get("description"),
            category=request.POST.get("category"),
            price=request.POST.get("price"),
            stock=request.POST.get("stock"),
            image=request.FILES.get("image")
        )

        return redirect(reverse("listings:dashboard") + "?fast=1")

    return render(request, "listings/add_product.html")

@login_required
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)

    # শুধু owner delete করতে পারবে
    if product.owner != request.user:
        return redirect("listings:dashboard")

    product.delete()
    return redirect("listings:dashboard")

@login_required
def buy_product(request, pk):
    product = get_object_or_404(Product, pk=pk)

    # নিজের প্রোডাক্ট কিনতে পারবে না
    if product.owner == request.user:
        return redirect("listings:dashboard")

    Order.objects.create(
        buyer=request.user,
        product=product
    )
    return redirect("listings:dashboard")


# 📦 PRODUCT DETAIL
@login_required
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)

    return render(request, "listings/detail.html", {
        "product": product
    })