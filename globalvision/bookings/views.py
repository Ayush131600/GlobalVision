from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings
from .models import Transaction, Booking
from .utils import generate_esewa_signature, format_amount, verify_esewa_payment
from django.contrib import messages

def initiate_esewa_payment(request, transaction_id):
    transaction = get_object_or_404(Transaction, id=transaction_id, user=request.user)
    
    # Amounts must be formatted exactly as required by eSewa (.2f or integer string)
    formatted_amount = format_amount(transaction.total_amount)
    formatted_zero = format_amount(0)
    
    # Generate signature using the EXACT 3-field chain from working sample
    signature = generate_esewa_signature(
        total_amount=formatted_amount,
        transaction_uuid=transaction.transaction_uuid,
        product_code=settings.ESEWA_PRODUCT_CODE
    )
    
    context = {
        'transaction': transaction,
        'esewa_url': settings.ESEWA_PAYMENT_URL,
        'product_code': settings.ESEWA_PRODUCT_CODE,
        'formatted_amount': formatted_amount,
        'formatted_zero': formatted_zero,
        'signature': signature,
        # Standard signed fields for v2
        'signed_field_names': 'total_amount,transaction_uuid,product_code',
        # Redirect URLs back to this app
        'success_url': request.build_absolute_uri('/bookings/esewa/success/'),
        'failure_url': request.build_absolute_uri('/bookings/esewa/failure/'),
    }
    
    return render(request, 'bookings/esewa_form.html', context)

def esewa_success(request):
    # eSewa v2 success returns data in the URL (GET) or as a base64 encoded string
    # See: https://developer.esewa.com.np/#/epay?id=payment-verification-amp-confirmation
    encoded_data = request.GET.get('data')
    if not encoded_data:
        messages.error(request, "Invalid payment response from eSewa.")
        return redirect('user_bookings')

    try:
        import base64
        import json
        decoded_data = base64.b64decode(encoded_data).decode('utf-8')
        data = json.loads(decoded_data)
        
        transaction_uuid = data.get('transaction_uuid')
        total_amount = data.get('total_amount')
        
        # Verify with eSewa server-to-server
        verification = verify_esewa_payment(
            product_code=settings.ESEWA_PRODUCT_CODE,
            total_amount=total_amount,
            transaction_uuid=transaction_uuid
        )
        
        if verification:
            # Update Transaction and Bookings
            tx = get_object_or_404(Transaction, transaction_uuid=transaction_uuid)
            tx.status = 'Success'
            tx.save()
            
            # Link bookings
            tx.bookings.update(payment_status='Paid', status='Confirmed')
            
            messages.success(request, f"Payment successful! Transaction ID: {data.get('transaction_code')}")
        else:
            messages.error(request, "Payment verification failed.")
            
    except Exception as e:
        messages.error(request, f"Error processing payment: {str(e)}")

    return redirect('user_bookings')

def esewa_failure(request):
    messages.error(request, "Payment was cancelled or failed. Please try again.")
    return redirect('user_cart')
