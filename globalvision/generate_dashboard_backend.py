import os

DASHBOARD_DIR = r'c:\Users\Acer\Desktop\GlobalVision\globalvision\dashboard'
TEMPLATES_DIR = r'c:\Users\Acer\Desktop\GlobalVision\globalvision\templates'
STATIC_DIR = r'c:\Users\Acer\Desktop\GlobalVision\globalvision\static\css'

os.makedirs(os.path.join(DASHBOARD_DIR), exist_ok=True)
os.makedirs(os.path.join(TEMPLATES_DIR, 'auth'), exist_ok=True)
os.makedirs(os.path.join(TEMPLATES_DIR, 'dashboard', 'vehicles'), exist_ok=True)
os.makedirs(os.path.join(TEMPLATES_DIR, 'dashboard', 'equipment'), exist_ok=True)
os.makedirs(os.path.join(TEMPLATES_DIR, 'dashboard', 'blog'), exist_ok=True)
os.makedirs(STATIC_DIR, exist_ok=True)

# 1. dashboard/models.py
with open(os.path.join(DASHBOARD_DIR, 'models.py'), 'w', encoding='utf-8') as f:
    f.write('''from django.db import models
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
''')

# 4. dashboard/decorators.py
with open(os.path.join(DASHBOARD_DIR, 'decorators.py'), 'w', encoding='utf-8') as f:
    f.write('''from functools import wraps
from django.shortcuts import redirect

def admin_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('admin_login')
        if not request.user.is_staff:
            return redirect('admin_login')
        return view_func(request, *args, **kwargs)
    return wrapper
''')

# 5. dashboard/forms.py
with open(os.path.join(DASHBOARD_DIR, 'forms.py'), 'w', encoding='utf-8') as f:
    f.write('''from django import forms
from .models import Vehicle, Equipment, BlogPost

class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ['name', 'type', 'description', 'price_per_day', 'is_available', 'image']

class EquipmentForm(forms.ModelForm):
    class Meta:
        model = Equipment
        fields = ['name', 'category', 'description', 'price_per_day', 'stock', 'image']

from django_summernote.widgets import SummernoteWidget
class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'content', 'cover_image', 'status']
        widgets = {
            'content': SummernoteWidget()
        }
''')

# 3. dashboard/urls.py
with open(os.path.join(DASHBOARD_DIR, 'urls.py'), 'w', encoding='utf-8') as f:
    f.write('''from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_home, name='dashboard_home'),
    
    path('vehicles/', views.vehicle_list, name='vehicle_list'),
    path('vehicles/add/', views.vehicle_add, name='vehicle_add'),
    path('vehicles/<int:pk>/edit/', views.vehicle_edit, name='vehicle_edit'),
    path('vehicles/<int:pk>/delete/', views.vehicle_delete, name='vehicle_delete'),
    
    path('equipment/', views.equipment_list, name='equipment_list'),
    path('equipment/add/', views.equipment_add, name='equipment_add'),
    path('equipment/<int:pk>/edit/', views.equipment_edit, name='equipment_edit'),
    path('equipment/<int:pk>/delete/', views.equipment_delete, name='equipment_delete'),
    
    path('blog/', views.blog_list, name='blog_list'),
    path('blog/add/', views.blog_add, name='blog_add'),
    path('blog/<int:pk>/edit/', views.blog_edit, name='blog_edit'),
    path('blog/<int:pk>/delete/', views.blog_delete, name='blog_delete'),
    
    path('about/', views.about_editor, name='about_editor'),
    path('contact/', views.contact_editor, name='contact_editor'),
    path('logout/', views.admin_logout_view, name='admin_logout'),
]
''')
