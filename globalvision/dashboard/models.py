from django.db import models
from django.conf import settings
from django.utils.text import slugify

class Vehicle(models.Model):
    CATEGORY_CHOICES = [
        ('Car', 'Car'),
        ('Jeep', 'Jeep'),
        ('Motorbike', 'Motorbike'),
        ('Bicycle', 'Bicycle'),
    ]
    STATUS_CHOICES = [
        ('Available', 'Available'),
        ('Rented', 'Rented'),
        ('Maintenance', 'Maintenance'),
    ]
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='Car')
    description = models.TextField()
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Available')
    image = models.ImageField(upload_to='vehicles/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

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

    def __str__(self):
        return self.name

class BlogPost(models.Model):
    title = models.CharField(max_length=300)
    slug = models.SlugField(unique=True, blank=True, default='')
    body = models.TextField(default='')
    cover_image = models.ImageField(upload_to='blog/', blank=True, null=True)
    category = models.CharField(max_length=100, default='General')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name='dashboard_posts')
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class ContactMessage(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    subject = models.CharField(max_length=300)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name}"

class AboutPage(models.Model):
    mission = models.TextField(default='')
    story = models.TextField(default='')
    stat_years = models.IntegerField(default=0, verbose_name="Years of Experience")
    stat_treks = models.IntegerField(default=0, verbose_name="Treks Completed")
    stat_clients = models.IntegerField(default=0, verbose_name="Happy Clients")
    stat_team = models.IntegerField(default=0, verbose_name="Team Members")
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "About Us Content"

class TeamMember(models.Model):
    name = models.CharField(max_length=200)
    role = models.CharField(max_length=200)
    favourite_trek = models.CharField(max_length=200, blank=True)
    photo = models.ImageField(upload_to='team/', blank=True, null=True)
    display_order = models.IntegerField(default=0)

    class Meta:
        ordering = ['display_order']

    def __str__(self):
        return self.name

class SiteSettings(models.Model):
    phone = models.CharField(max_length=20, blank=True)
    whatsapp = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    maps_embed = models.TextField(blank=True)
    hours = models.CharField(max_length=200, blank=True)
    facebook_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    tripadvisor_url = models.URLField(blank=True)

    class Meta:
        verbose_name = "Site Settings"

class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ]
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='dashboard_bookings'
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