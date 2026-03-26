from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from .decorators import admin_required
from inventory.models import Vehicle, Equipment
from bookings.models import Booking
from blog.models import BlogPost
from cms.models import TeamMember, AboutPage, SiteSettings
from contacts.models import ContactMessage
from .forms import VehicleForm, EquipmentForm, BlogPostForm, TeamMemberForm, AboutPageForm, SiteSettingsForm
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
            if user.is_staff or user.role == 'admin':
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
        'total_blogs': BlogPost.objects.count(),
        'unread_messages': ContactMessage.objects.filter(is_read=False).count(),
        'total_bookings': Booking.objects.count(),
        'total_users': User.objects.count(),
        'recent_bookings': Booking.objects.all().order_by('-id')[:5],
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
        post.author = request.user
        post.save()
        return redirect('blog_list')
    return render(request, 'dashboard/blog/form.html', {'form': form, 'title': 'Write Post'})

@admin_required
def blog_edit(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    form = BlogPostForm(request.POST or None, request.FILES or None, instance=post)
    if form.is_valid():
        form.save()
        return redirect('blog_list')
    return render(request, 'dashboard/blog/form.html', {'form': form, 'title': 'Edit Post', 'object': post})

@require_http_methods(["POST"])
@admin_required
def blog_delete(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    post.delete()
    return redirect('blog_list')

@admin_required
def blog_approve(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    post.status = 'accepted'
    post.is_published = True
    post.save()
    return redirect('blog_list')

@admin_required
def blog_reject(request, pk):
    if request.method == 'POST':
        post = get_object_or_404(BlogPost, pk=pk)
        reason = request.POST.get('reason')
        if reason:
            post.status = 'rejected'
            post.is_published = False
            post.rejection_reason = reason
            post.save()
    return redirect('blog_list')

@admin_required
def contact_message_list(request):
    messages = ContactMessage.objects.all().order_by('-created_at')
    return render(request, 'dashboard/contact/list.html', {'messages': messages})


@admin_required
def contact_message_detail(request, pk):
    message = get_object_or_404(ContactMessage, pk=pk)
    # Mark as read
    if not message.is_read:
        message.is_read = True
        message.save()
    return render(request, 'dashboard/contact/detail.html', {'message': message})

@require_http_methods(["POST"])
@admin_required
def contact_message_delete(request, pk):
    message = get_object_or_404(ContactMessage, pk=pk)
    message.delete()
    return redirect('contact_list')

@admin_required
def about_editor(request):
    about_obj = AboutPage.objects.first()
    if not about_obj:
        about_obj = AboutPage.objects.create(
            mission='', story='', stat_years=0, stat_treks=0, stat_clients=0, stat_team=0
        )
    
    if request.method == 'POST':
        form = AboutPageForm(request.POST, request.FILES, instance=about_obj)
        if form.is_valid():
            form.save()
            return redirect('about_editor')
    else:
        form = AboutPageForm(instance=about_obj)
        
    team_members = TeamMember.objects.all().order_by('display_order')
    return render(request, 'dashboard/about.html', {
        'form': form,
        'team_members': team_members
    })

@admin_required
def site_settings(request):
    settings_obj = SiteSettings.objects.first()
    if not settings_obj:
        settings_obj = SiteSettings.objects.create()
        
    if request.method == 'POST':
        form = SiteSettingsForm(request.POST, instance=settings_obj)
        if form.is_valid():
            form.save()
            return redirect('site_settings')
    else:
        form = SiteSettingsForm(instance=settings_obj)
        
    return render(request, 'dashboard/settings.html', {'form': form})