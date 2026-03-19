import os

BASE_DIR = r"c:\Users\Acer\Desktop\GlobalVision\globalvision"

files_to_write = {}

files_to_write["dashboard/models.py"] = """from django.db import models
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
"""

files_to_write["dashboard/views.py"] = """from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from .decorators import admin_required
from .models import Vehicle, Equipment, Booking, BlogPost, TeamMember, AboutContent, SiteSettings
from .forms import VehicleForm, EquipmentForm, BlogPostForm
from django.contrib.auth import get_user_model

@require_http_methods(["GET", "POST"])
def admin_login_view(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('dashboard_home')
    
    error = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_staff:
                login(request, user)
                return redirect('dashboard_home')
            else:
                error = 'You are not authorized as admin.'
        else:
            error = 'Invalid username or password.'
    
    return render(request, 'auth/admin_login.html', {'error': error})

def admin_logout_view(request):
    logout(request)
    return redirect('admin_login')

@admin_required
def dashboard_home(request):
    User = get_user_model()
    context = {
        'total_vehicles': Vehicle.objects.count(),
        'total_equipment': Equipment.objects.count(),
        'total_bookings': Booking.objects.filter(
            created_at__date=timezone.now().date()
        ).count(),
        'total_users': User.objects.filter(is_staff=False).count(),
        'recent_bookings': Booking.objects.select_related(
            'user', 'vehicle'
        ).order_by('-created_at')[:8],
    }
    return render(request, 'dashboard/home.html', context)

@admin_required
def vehicle_list(request):
    vehicles = Vehicle.objects.all().order_by('-created_at')
    return render(request, 'dashboard/vehicles/list.html', {'vehicles': vehicles})

@admin_required
def vehicle_add(request):
    form = VehicleForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect('vehicle_list')
    return render(request, 'dashboard/vehicles/form.html', {'form': form, 'title': 'Add Vehicle'})

@admin_required
def vehicle_edit(request, pk):
    vehicle = get_object_or_404(Vehicle, pk=pk)
    form = VehicleForm(request.POST or None, request.FILES or None, instance=vehicle)
    if form.is_valid():
        form.save()
        return redirect('vehicle_list')
    return render(request, 'dashboard/vehicles/form.html', {'form': form, 'title': 'Edit Vehicle', 'object': vehicle})

@require_http_methods(["POST"])
@admin_required
def vehicle_delete(request, pk):
    vehicle = get_object_or_404(Vehicle, pk=pk)
    vehicle.delete()
    return redirect('vehicle_list')

@admin_required
def equipment_list(request):
    equipment = Equipment.objects.all().order_by('-created_at')
    return render(request, 'dashboard/equipment/list.html', {'equipment': equipment})

@admin_required
def equipment_add(request):
    form = EquipmentForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect('equipment_list')
    return render(request, 'dashboard/equipment/form.html', {'form': form, 'title': 'Add Equipment'})

@admin_required
def equipment_edit(request, pk):
    equipment = get_object_or_404(Equipment, pk=pk)
    form = EquipmentForm(request.POST or None, request.FILES or None, instance=equipment)
    if form.is_valid():
        form.save()
        return redirect('equipment_list')
    return render(request, 'dashboard/equipment/form.html', {'form': form, 'title': 'Edit Equipment', 'object': equipment})

@require_http_methods(["POST"])
@admin_required
def equipment_delete(request, pk):
    equipment = get_object_or_404(Equipment, pk=pk)
    equipment.delete()
    return redirect('equipment_list')

@admin_required
def blog_list(request):
    posts = BlogPost.objects.all().order_by('-created_at')
    return render(request, 'dashboard/blog/list.html', {'posts': posts})

@admin_required
def blog_add(request):
    form = BlogPostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        post = form.save(commit=False)
        if post.status == 'published' and not post.published_at:
            post.published_at = timezone.now()
        post.save()
        return redirect('blog_list')
    return render(request, 'dashboard/blog/form.html', {'form': form, 'title': 'Write Post'})

@admin_required
def blog_edit(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    form = BlogPostForm(request.POST or None, request.FILES or None, instance=post)
    if form.is_valid():
        post = form.save(commit=False)
        if post.status == 'published' and not post.published_at:
            post.published_at = timezone.now()
        post.save()
        return redirect('blog_list')
    return render(request, 'dashboard/blog/form.html', {'form': form, 'title': 'Edit Post', 'object': post})

@require_http_methods(["POST"])
@admin_required
def blog_delete(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    post.delete()
    return redirect('blog_list')

@admin_required
def about_editor(request):
    about = AboutContent.objects.first()
    if not about:
        about = AboutContent.objects.create(
            tagline='', company_story='', mission_statement='',
            stat_trekkers=0, stat_vehicles=0, stat_equipment=0
        )
    team_members = TeamMember.objects.all().order_by('order')
    
    if request.method == 'POST':
        about.tagline = request.POST.get('tagline')
        about.company_story = request.POST.get('company_story')
        about.mission_statement = request.POST.get('mission_statement')
        about.stat_trekkers = request.POST.get('stat_trekkers', 0)
        about.stat_vehicles = request.POST.get('stat_vehicles', 0)
        about.stat_equipment = request.POST.get('stat_equipment', 0)
        about.save()
        
        # Determine how many members we have to loop through based on the JS additions
        # First process the ones directly submitted by id in POST keys for existing or deleted ones
        delete_ids = request.POST.get('delete_members', '').split(',')
        if delete_ids:
            for d in delete_ids:
                if d.strip().isdigit():
                    TeamMember.objects.filter(id=int(d)).delete()
                    
        # Iterate post data keys using a pattern like member_X_name
        for key in request.POST.keys():
            if key.startswith('member_') and key.endswith('_name'):
                mid = key.split('_')[1]
                if mid.isdigit():
                    tm = TeamMember.objects.filter(id=int(mid)).first()
                    if tm:
                        tm.name = request.POST.get(f'member_{mid}_name', tm.name)
                        tm.role = request.POST.get(f'member_{mid}_role', tm.role)
                        tm.bio = request.POST.get(f'member_{mid}_bio', tm.bio)
                        tm.favorite_trek = request.POST.get(f'member_{mid}_fav', tm.favorite_trek)
                        if request.FILES.get(f'member_{mid}_photo'):
                            tm.photo = request.FILES.get(f'member_{mid}_photo')
                        tm.save()
            elif key.startswith('new_member_') and key.endswith('_name'):
                temp_id = key.split('_')[2]
                name = request.POST.get(key)
                if name:
                    TeamMember.objects.create(
                        name=name,
                        role=request.POST.get(f'new_member_{temp_id}_role', ''),
                        bio=request.POST.get(f'new_member_{temp_id}_bio', ''),
                        favorite_trek=request.POST.get(f'new_member_{temp_id}_fav', ''),
                        photo=request.FILES.get(f'new_member_{temp_id}_photo')
                    )
        
        return redirect('about_editor')
    
    return render(request, 'dashboard/about.html', {
        'about': about,
        'team_members': team_members
    })

@admin_required
def contact_editor(request):
    settings_obj = SiteSettings.objects.first()
    if not settings_obj:
        settings_obj = SiteSettings.objects.create(
            phone='', email='', address='',
            maps_embed='', whatsapp='', opening_hours=''
        )
    if request.method == 'POST':
        settings_obj.phone = request.POST.get('phone')
        settings_obj.email = request.POST.get('email')
        settings_obj.address = request.POST.get('address')
        settings_obj.maps_embed = request.POST.get('maps_embed')
        settings_obj.whatsapp = request.POST.get('whatsapp')
        settings_obj.opening_hours = request.POST.get('opening_hours')
        settings_obj.save()
        return redirect('contact_editor')
    return render(request, 'dashboard/contact.html', {'settings': settings_obj})
"""

files_to_write["dashboard/urls.py"] = """from django.urls import path
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
"""

files_to_write["dashboard/decorators.py"] = """from functools import wraps
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
"""

files_to_write["dashboard/forms.py"] = """from django import forms
from .models import Vehicle, Equipment, BlogPost
from django.core.exceptions import ValidationError
import os
from django_summernote.widgets import SummernoteWidget

def validate_image_extension(value):
    ext = os.path.splitext(value.name)[1].lower()
    valid_extensions = ['.jpg', '.jpeg', '.png', '.webp']
    if ext not in valid_extensions:
        raise ValidationError('Only JPG, JPEG, PNG, and WEBP files are allowed.')

class VehicleForm(forms.ModelForm):
    image = forms.ImageField(validators=[validate_image_extension], required=False)
    class Meta:
        model = Vehicle
        fields = ['name', 'type', 'description', 'price_per_day', 'is_available', 'image']

class EquipmentForm(forms.ModelForm):
    image = forms.ImageField(validators=[validate_image_extension], required=False)
    class Meta:
        model = Equipment
        fields = ['name', 'category', 'description', 'price_per_day', 'stock', 'image']

class BlogPostForm(forms.ModelForm):
    cover_image = forms.ImageField(validators=[validate_image_extension], required=False)
    class Meta:
        model = BlogPost
        fields = ['title', 'content', 'cover_image', 'status']
        widgets = {
            'content': SummernoteWidget()
        }
"""

import os
for rel_path, content in files_to_write.items():
    full_path = os.path.join(BASE_DIR, rel_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\\n")
    print(f"Wrote {full_path}")
