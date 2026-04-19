from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.conf import settings
from datetime import date

class Vehicle(models.Model):
    CATEGORY_CHOICES = [
        ('Luxury', 'Luxury'),
        ('Off Road', 'Off Road'),
        ('Vans', 'Vans'),
    ]
    STATUS_CHOICES = [
        ('Available', 'Available'),
        ('Rented', 'Rented'),
        ('Maintenance', 'Maintenance'),
    ]
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='Luxury')
    description = models.TextField()
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Available')
    stock = models.IntegerField(default=1)
    image = models.ImageField(upload_to='vehicles/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.stock <= 0:
            self.status = 'Rented' if self.status == 'Rented' else 'Maintenance' if self.status == 'Maintenance' else 'Rented'
            # Actually, if stock is 0, it should probably be 'Rented' or 'Not Available'.
            # The current status choices are 'Available', 'Rented', 'Maintenance'.
            # If stock is 0, we can set it to 'Rented' (as in all units are rented).
            if self.status == 'Available':
                self.status = 'Rented'
        elif self.status == 'Rented' and self.stock > 0:
            self.status = 'Available'
        super().save(*args, **kwargs)

    @property
    def is_rented_today(self):
        from bookings.models import Booking
        today = date.today()
        count = Booking.objects.filter(
            content_type=ContentType.objects.get_for_model(self.__class__),
            object_id=self.id,
            status__in=['Confirmed', 'Active'],
            start_date__lte=today,
            end_date__gte=today
        ).count()
        return count >= self.stock

    def __str__(self):
        return self.name

class Equipment(models.Model):
    CATEGORY_CHOICES = [
        ('Trekking', 'Trekking'),
        ('Camping', 'Camping'),
        ('Climbing', 'Climbing'),
        ('Safety', 'Safety'),
    ]
    STATUS_CHOICES = [
        ('Available', 'Available'),
        ('Out of Stock', 'Out of Stock'),
    ]
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='Trekking')
    description = models.TextField()
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Available')
    image = models.ImageField(upload_to='equipment/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


    def save(self, *args, **kwargs):
        if self.stock <= 0:
            self.status = 'Out of Stock'
        elif self.status == 'Out of Stock' and self.stock > 0:
            self.status = 'Available'
        super().save(*args, **kwargs)

    @property
    def is_rented_today(self):
        from bookings.models import Booking
        today = date.today()
        count = Booking.objects.filter(
            content_type=ContentType.objects.get_for_model(self.__class__),
            object_id=self.id,
            status__in=['Confirmed', 'Active'],
            start_date__lte=today,
            end_date__gte=today
        ).count()
        return count >= self.stock

    def __str__(self):
        return self.name

class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Review by {self.user.user_name} for {self.content_object}"
