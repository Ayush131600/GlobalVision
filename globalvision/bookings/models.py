from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
import uuid

class Transaction(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Success', 'Success'),
        ('Failed', 'Failed'),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    transaction_uuid = models.CharField(max_length=100, unique=True, default=uuid.uuid4)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Transaction {self.transaction_uuid} - {self.status}"

class Booking(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Active', 'Active'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]
    PAYMENT_STATUS_CHOICES = [
        ('Unpaid', 'Unpaid'),
        ('Paid', 'Paid'),
        ('Failed', 'Failed'),
    ]
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='bookings'
    )
    
    # Generic relation to Vehicle or Equipment
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    item = GenericForeignKey('content_type', 'object_id')
    
    @property
    def item_type(self):
        return self.content_type.model if self.content_type else None

    @property
    def item_id(self):
        return self.object_id

    start_date = models.DateField()
    end_date = models.DateField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='Pending'
    )
    payment_status = models.CharField(
        max_length=20, choices=PAYMENT_STATUS_CHOICES, default='Unpaid'
    )
    transaction = models.ForeignKey(
        Transaction, on_delete=models.SET_NULL, null=True, blank=True, related_name='bookings'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Booking #{self.id} - {self.user}"

def get_unavailable_dates(item):
    """Returns a list of dates (strings) where the item is fully booked."""
    from datetime import date, timedelta
    from django.db.models import Count
    
    today = date.today()
    # Check for the next 6 months to keep it performant
    check_days = 180
    
    # Pre-fetch overlapping bookings to avoid DB hits in loop
    bookings = Booking.objects.filter(
        content_type=ContentType.objects.get_for_model(item),
        object_id=item.id,
        status__in=['Confirmed', 'Active'],
        end_date__gte=today
    )
    
    unavailable_dates = []
    
    # Optimize: If stock is 1, any date between start and end is unavailable
    if item.stock == 1:
        for b in bookings:
            curr = max(b.start_date, today)
            while curr <= b.end_date:
                unavailable_dates.append(curr.strftime('%Y-%m-%d'))
                curr += timedelta(days=1)
    else:
        # For multiple stock, we need to count for each day
        for i in range(check_days):
            current_date = today + timedelta(days=i)
            count = bookings.filter(start_date__lte=current_date, end_date__gte=current_date).count()
            if count >= item.stock:
                unavailable_dates.append(current_date.strftime('%Y-%m-%d'))
                
    return sorted(list(set(unavailable_dates)))

def is_item_available(item, start_date, end_date):
    """Checks if the item is available for the given date range."""
    from datetime import datetime
    
    if isinstance(start_date, str):
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
    if isinstance(end_date, str):
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        
    # Get all overlapping bookings
    bookings = Booking.objects.filter(
        content_type=ContentType.objects.get_for_model(item),
        object_id=item.id,
        status__in=['Confirmed', 'Active']
    ).filter(
        models.Q(start_date__lte=end_date) & models.Q(end_date__gte=start_date)
    )
    
    if item.stock == 1:
        return not bookings.exists()
    
    # Check each day in range
    from datetime import timedelta
    curr = start_date
    while curr <= end_date:
        count = bookings.filter(start_date__lte=curr, end_date__gte=curr).count()
        if count >= item.stock:
            return False
        curr += timedelta(days=1)
        
    return True
