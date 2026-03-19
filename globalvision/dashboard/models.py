from django.db import models
from django.conf import settings

class Vehicle(models.Model):
    TYPE_CHOICES = [
        ('car', 'Car'),
        ('jeep', 'Jeep'),
        ('motorbike', 'Motorbike'),
        ('bicycle', 'Bicycle'),
    ]
    name = models.CharField(max_length=200)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    description = models.TextField()
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    is_available = models.BooleanField(default=True)
    image = models.ImageField(upload_to='vehicles/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Equipment(models.Model):
    CATEGORY_CHOICES = [
        ('trekking', 'Trekking'),
        ('camping', 'Camping'),
        ('climbing', 'Climbing'),
        ('safety', 'Safety'),
    ]
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    description = models.TextField()
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    image = models.ImageField(upload_to='equipment/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class BlogPost(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
    ]
    title = models.CharField(max_length=300)
    content = models.TextField()
    cover_image = models.ImageField(upload_to='blog/')
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default='draft'
    )
    published_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class TeamMember(models.Model):
    name = models.CharField(max_length=200)
    role = models.CharField(max_length=200)
    bio = models.TextField()
    favorite_trek = models.CharField(max_length=200)
    photo = models.ImageField(upload_to='team/')
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name

class AboutContent(models.Model):
    tagline = models.CharField(max_length=300)
    company_story = models.TextField()
    mission_statement = models.TextField()
    stat_trekkers = models.IntegerField(default=0)
    stat_vehicles = models.IntegerField(default=0)
    stat_equipment = models.IntegerField(default=0)

    class Meta:
        verbose_name = "About Content"

    def __str__(self):
        return "About Us Content"

class SiteSettings(models.Model):
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    address = models.TextField()
    maps_embed = models.TextField()
    whatsapp = models.CharField(max_length=20)
    opening_hours = models.TextField()

    class Meta:
        verbose_name = "Site Settings"

    def __str__(self):
        return "Site Settings"

class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ]
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='bookings'
    )
    vehicle = models.ForeignKey(
        Vehicle, null=True, blank=True, on_delete=models.SET_NULL
    )
    start_date = models.DateField()
    end_date = models.DateField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default='pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking #{self.id} - {self.user}"