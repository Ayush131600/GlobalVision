from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from .models import Vehicle, Equipment, Review
from .forms import ReviewForm
from django.contrib import messages

@login_required
def add_review(request, product_type, product_id):
    if product_type == 'vehicle':
        product = get_object_or_404(Vehicle, id=product_id)
        content_type = ContentType.objects.get_for_model(Vehicle)
    else:
        product = get_object_or_404(Equipment, id=product_id)
        content_type = ContentType.objects.get_for_model(Equipment)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.content_type = content_type
            review.object_id = product_id
            review.save()
            messages.success(request, "Your review has been submitted!")
        else:
            messages.error(request, "There was an error with your review.")
    
    return redirect('account:product_detail', product_type=product_type, product_id=product_id)

@login_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    
    # Permission check: Only the owner or an admin can delete
    if review.user == request.user or request.user.is_staff:
        product_type = 'vehicle' if isinstance(review.content_object, Vehicle) else 'equipment'
        product_id = review.object_id
        
        review.delete()
        messages.success(request, "Review deleted successfully.")
        return redirect('account:product_detail', product_type=product_type, product_id=product_id)
    else:
        messages.error(request, "You do not have permission to delete this review.")
        return redirect('home')
