from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from .models import Cart, CartItem
from inventory.models import Vehicle, Equipment

@login_required(login_url='account:login')
def add_to_cart(request, product_type, product_id):
    if product_type == 'vehicle':
        product = get_object_or_404(Vehicle, id=product_id)
        content_type = ContentType.objects.get_for_model(Vehicle)
    elif product_type == 'equipment':
        product = get_object_or_404(Equipment, id=product_id)
        content_type = ContentType.objects.get_for_model(Equipment)
    else:
        messages.error(request, "Invalid product type.")
        return redirect('home')

    cart, created = Cart.objects.get_or_create(user=request.user)
    
    # Check if item already exists in cart
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart, 
        content_type=content_type, 
        object_id=product_id
    )

    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        if start_date:
            cart_item.start_date = start_date
        if end_date:
            cart_item.end_date = end_date
        cart_item.save()

    if not created:
        messages.info(request, f"{product.name} is already in your cart.")
    else:
        messages.success(request, f"{product.name} added to cart.")

    return redirect('user_cart')
