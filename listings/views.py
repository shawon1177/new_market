


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import FoodItem,CATEGORY_CHOICES

def food_list(request):
    category = request.GET.get('category')

    foods = FoodItem.objects.filter(availability_status=True)

    if category:
        foods = foods.filter(category=category)

    foods = foods.select_related('seller').order_by('-created_at')

    return render(request, 'listings/food_list.html', {
        'foods': foods,
        'categories': CATEGORY_CHOICES
    })

@login_required
def create_food(request):
    if request.method == "POST":
        FoodItem.objects.create(
            seller=request.user,
            title=request.POST.get('title'),
            description=request.POST.get('description'),
            price=request.POST.get('price'),
            image=request.FILES.get('image'),
            category=request.POST.get('category'),
            availability_status=True
        )
        return redirect('food_list')

    return render(request, 'listings/create_food.html', {
        'categories': CATEGORY_CHOICES
    })