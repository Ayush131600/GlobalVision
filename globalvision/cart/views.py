from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from .models import Cart, CartItem
from inventory.models import Vehicle, Equipment
from bookings.models import Booking, is_item_available

def add_to_cart(request, product_type, product_id):
    # If user is not authenticated, save their selection to session and redirect
    if not request.user.is_authenticated:
        if request.method == 'POST':
            # Save the rental details in session to pick up after login
            request.session['pending_rental'] = {
                'product_type': product_type,
                'product_id': product_id,
                'start_date': request.POST.get('start_date'),
                'end_date': request.POST.get('end_date')
            }
        
        # Prepare login redirect with 'next' parameter pointing back to this same view
        from django.urls import reverse
        login_url = reverse('account:login')
        current_path = request.get_full_path()
        return redirect(f"{login_url}?next={current_path}")

    # Handle product identification
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
    cart_item, item_created = CartItem.objects.get_or_create(
        cart=cart, 
        content_type=content_type, 
        object_id=product_id
    )

    # Use data from POST or from session (if it was a pending rental)
    start_date = None
    end_date = None

    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
    
    # Check session for pending rental data for THIS product
    pending = request.session.get('pending_rental')
    if pending and pending['product_id'] == product_id and pending['product_type'] == product_type:
        if not start_date: start_date = pending.get('start_date')
        if not end_date: end_date = pending.get('end_date')
        # Clear the pending rental from session now that we've processed it
        del request.session['pending_rental']

    if start_date:
        cart_item.start_date = start_date
    if end_date:
        cart_item.end_date = end_date
    
    # NEW: Check if the item is available for these dates
    if start_date and end_date:
        if not is_item_available(product, start_date, end_date):
            messages.error(request, f"Sorry, {product.name} is already booked for the selected dates.")
            if item_created:
                cart_item.delete()
            return redirect('account:product_detail', product_type=product_type, product_id=product_id)

    cart_item.save()

    if not item_created:
        messages.info(request, f"{product.name} is already in your cart (dates updated).")
    else:
        messages.success(request, f"{product.name} added to cart.")

    return redirect('user_cart')
