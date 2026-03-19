from django.shortcuts import render, redirect, get_object_or_404
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
        try:
            about.stat_trekkers = int(request.POST.get('stat_trekkers') or 0)
            about.stat_vehicles = int(request.POST.get('stat_vehicles') or 0)
            about.stat_equipment = int(request.POST.get('stat_equipment') or 0)
        except ValueError:
            pass
        about.save()
        
        # Determine how many members we have to loop through based on the JS additions
        # First process the ones directly submitted by id in POST keys for existing or deleted ones
        delete_ids = request.POST.get('delete_members', '').split(',')
        if delete_ids:
            for d in delete_ids:
                if d.strip().isdigit():
                    TeamMember.objects.filter(id=int(d)).delete()
                    
        # Handle editing existing members that were rendered correctly as member_{id}_name
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
            elif key.startswith('new_member_name_'):
                # Key is something like new_member_name_1
                temp_id = key.split('_')[-1]
                name = request.POST.get(key)
                if name:
                    tm = TeamMember.objects.create(
                        name=name,
                        role=request.POST.get(f'new_member_role_{temp_id}', ''),
                        bio=request.POST.get(f'new_member_bio_{temp_id}', ''),
                        favorite_trek=request.POST.get(f'new_member_fav_{temp_id}', '')
                    )
                    if request.FILES.get(f'new_member_photo_{temp_id}'):
                        tm.photo = request.FILES.get(f'new_member_photo_{temp_id}')
                        tm.save()
        
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