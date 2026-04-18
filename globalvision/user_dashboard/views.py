from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.db import transaction
from django.utils import timezone
from .decorators import user_required
from bookings.models import Booking, Transaction
from cart.models import Cart, CartItem
from contacts.models import ContactMessage
from inventory.models import Vehicle, Equipment
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from decimal import Decimal
from notifications.utils import create_notification

@user_required
def user_overview(request):
    user = request.user
    
    # Live summary stats
    active_bookings_count = Booking.objects.filter(user=user).exclude(status__in=['Completed', 'Cancelled']).count()
    past_bookings_count = Booking.objects.filter(user=user, status__in=['Completed', 'Cancelled']).count()
    
    # Cart items
    cart, created = Cart.objects.get_or_create(user=user)
    cart_items_count = cart.items.count()
    
    # Support tickets
    support_tickets_count = ContactMessage.objects.filter(user=user).count()
    
    context = {
        'active_bookings': active_bookings_count,
        'past_bookings': past_bookings_count,
        'cart_items': cart_items_count,
        'support_tickets': support_tickets_count,
    }
    return render(request, 'user_dashboard/overview.html', context)

@user_required
def user_profile(request):
    user = request.user
    if request.method == 'POST':
        if 'update_profile' in request.POST:
            user.user_name = request.POST.get('user_name')
            user.email = request.POST.get('email')
            user.phone_no = request.POST.get('phone_no')
            user.address = request.POST.get('address')
            user.dob = request.POST.get('dob') or None
            
            if request.FILES.get('profile_photo'):
                user.profile_photo = request.FILES.get('profile_photo')
            
            user.save()
            messages.success(request, "Profile is successfully updated.")
            return redirect('user_profile')
            
        elif 'change_password' in request.POST:
            form = PasswordChangeForm(user, request.POST)
            if form.is_valid():
                user_obj = form.save()
                update_session_auth_hash(request, user_obj)
                messages.success(request, "Password changed successfully.")
                return redirect('user_profile')
            else:
                messages.error(request, "Error changing password. Please check the details.")
    else:
        form = PasswordChangeForm(user)
        
    return render(request, 'user_dashboard/profile.html', {'password_form': form})

@user_required
def user_bookings(request):
    # Fetch active and upcoming bookings
    # Status is not Completed or Cancelled
    bookings = Booking.objects.filter(
        user=request.user
    ).exclude(
        status__in=['Completed', 'Cancelled']
    ).order_by('-created_at')
    
    return render(request, 'user_dashboard/bookings.html', {'bookings': bookings})

@user_required
def user_history(request):
    # Fetch completed and cancelled bookings
    status_filter = request.GET.get('status', 'All')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    
    query = Q(user=request.user)
    
    if status_filter == 'Completed':
        query &= Q(status='Completed')
    elif status_filter == 'Cancelled':
        query &= Q(status='Cancelled')
    else:
        query &= Q(status__in=['Completed', 'Cancelled'])
        
    if start_date:
        query &= Q(start_date__gte=start_date)
    if end_date:
        query &= Q(end_date__lte=end_date)
        
    bookings = Booking.objects.filter(query).order_by('-created_at')
    
    return render(request, 'user_dashboard/history.html', {
        'bookings': bookings,
        'current_status': status_filter,
        'start_date': start_date,
        'end_date': end_date
    })

@user_required
def user_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    items = cart.items.all()
    
    total_price = sum(item.total_price for item in items)
    
    return render(request, 'user_dashboard/cart.html', {
        'items': items,
        'total_price': total_price
    })

@user_required
def user_support(request):
    if request.method == 'POST':
        subject = request.POST.get('subject')
        message_body = request.POST.get('message')
        
        if subject and message_body:
            ContactMessage.objects.create(
                user=request.user,
                name=request.user.user_name,
                email=request.user.email,
                phone=request.user.phone_no,
                subject=subject,
                message=message_body,
                status='Open'
            )
            messages.success(request, "Support ticket submitted successfully.")
            return redirect('user_support')
        else:
            messages.error(request, "Both subject and message are required.")
            
    messages_list = ContactMessage.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'user_dashboard/support.html', {'support_messages': messages_list})

@user_required
def user_logout(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('account:login')

# Actions
@user_required
def cancel_booking(request, pk):
    if request.method != 'POST':
        messages.error(request, "Invalid request method.")
        return redirect('user_bookings')
        
    try:
        booking = Booking.objects.get(pk=pk, user=request.user)
    except Booking.DoesNotExist:
        messages.error(request, "Booking not found.")
        return redirect('user_bookings')

    if booking.status != 'Pending':
        messages.error(request, f"This booking is {booking.status.lower()} and cannot be cancelled.")
        return redirect('user_bookings')

    # Proceed with cancellation
    booking.status = 'Cancelled'
    booking.save()
    
    # Trigger notification
    create_notification(
        user=request.user,
        title="Booking Cancelled",
        message=f"Your booking for {booking.item.name if booking.item else 'Item'} has been cancelled.",
        type='general'
    )
    
    messages.success(request, "Booking cancelled successfully.")
    return redirect('user_bookings')

@user_required
def remove_from_cart(request, pk):
    if request.method != 'POST':
        return redirect('user_cart')
    # Ensure the user's cart exists
    cart, _ = Cart.objects.get_or_create(user=request.user)
    try:
        cart_item = CartItem.objects.get(pk=pk, cart=cart)
        cart_item.delete()
        messages.success(request, "Item removed from cart.")
    except CartItem.DoesNotExist:
        messages.error(request, "Item not found in your cart.")
    return redirect('user_cart')

@user_required
def update_cart_dates(request, pk):
    if request.method == 'POST':
        cart_item = get_object_or_404(CartItem, pk=pk, cart__user=request.user)
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        
        if start_date and end_date:
            cart_item.start_date = start_date
            cart_item.end_date = end_date
            cart_item.save()
            messages.success(request, "Dates updated.")
        else:
            messages.error(request, "Both dates are required.")
            
    return redirect('user_cart')

@user_required
def cart_checkout(request):
    cart = get_object_or_404(Cart, user=request.user)
    items = cart.items.all()
    
    if not items:
        messages.error(request, "Your cart is empty.")
        return redirect('user_cart')
        
    # Validate dates
    for item in items:
        if not item.start_date or not item.end_date:
            messages.error(request, f"Please select rental dates for {item.content_object.name}.")
            return redirect('user_cart')
            
    try:
        import uuid
        
        with transaction.atomic():
            # Create a master Transaction record
            total_sum = sum(item.total_price for item in items)
            tx = Transaction.objects.create(
                user=request.user,
                total_amount=total_sum,
                status='Pending'
            )
            
            # Use standard UUID format with dashes (working sample)
            tx.transaction_uuid = str(uuid.uuid4())
            tx.save()

            for item in items:
                Booking.objects.create(
                    user=request.user,
                    transaction=tx,
                    content_type=item.content_type,
                    object_id=item.object_id,
                    start_date=item.start_date,
                    end_date=item.end_date,
                    total_price=item.total_price,
                    status='Pending',
                    payment_status='Unpaid'
                )
            
            # Clear cart
            items.delete()
            
        return redirect('initiate_esewa_payment', transaction_id=tx.id)
    except Exception as e:
        messages.error(request, f"An error occurred during checkout: {str(e)}")
        return redirect('user_cart')
