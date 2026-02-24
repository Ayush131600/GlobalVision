from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Q
from .models import User, Vehicle, Equipment, BlogPost
from .forms import VehicleForm, EquipmentForm, BlogPostForm, UserProfileForm


def login(request):
    if request.method == "POST":
        user_name = request.POST.get("user_name")
        password = request.POST.get("password")

        user = authenticate(request, user_name=user_name, password=password)

        if user is not None:
            auth_login(request, user)
            return redirect("home")
        else:
            messages.error(
                request,
                "Invalid username or password",
                extra_tags="error"
            )

    return render(request, "account/login.html")


def admin_login(request):
    if request.method == "POST":
        user_name = request.POST.get("user_name")
        password = request.POST.get("password")

        user = authenticate(request, user_name=user_name, password=password)

        if user is not None and user.role == 'admin':
            auth_login(request, user)
            return redirect("account:dashboard")
        else:
            messages.error(
                request,
                "Invalid admin credentials or unauthorized access",
                extra_tags="error"
            )

    return render(request, "account/admin_login.html")





def register(request):
    if request.method == "POST":
        user_name = request.POST.get("user_name")
        email = request.POST.get("email")
        phone_no = request.POST.get("phone_no")
        dob = request.POST.get("dob")
        address = request.POST.get("address")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:
            messages.error(
                request,
                "Passwords do not match",
                extra_tags="error"
            )
            return redirect("register")

        if User.objects.filter(user_name=user_name).exists():
            messages.error(
                request,
                "Username already exists",
                extra_tags="error"
            )
            return redirect("register")

        if User.objects.filter(email=email).exists():
            messages.error(
                request,
                "Email already exists",
                extra_tags="error"
            )
            return redirect("register")

        if User.objects.filter(phone_no=phone_no).exists():
            messages.error(
                request,
                "Phone number already exists",
                extra_tags="error"
            )
            return redirect("register")

        user = User.objects.create_user(
            user_name=user_name,
            email=email,
            phone_no=phone_no,
            dob=dob,
            address=address,
            password=password
        )

        messages.success(
            request,
            "Registration successful",
            extra_tags="success"
        )

        auth_login(request, user)
        auth_login(request, user)
        return redirect("home")

    return render(request, "account/register.html")

from django.contrib.auth import logout as auth_logout

def logout_view(request):
    auth_logout(request)
    return redirect("home")
def home(request):
    query = request.GET.get('q', '').strip()
    if query:
        # Check for vehicle match
        vehicle = Vehicle.objects.filter(name__icontains=query).first()
        if vehicle:
            return redirect('account:product_detail', product_type='vehicle', product_id=vehicle.id)
        
        # Check for equipment match
        equipment = Equipment.objects.filter(name__icontains=query).first()
        if equipment:
            return redirect('account:product_detail', product_type='equipment', product_id=equipment.id)

    vehicles = Vehicle.objects.all()[:4]
    equipment = Equipment.objects.all()[:4]
    return render(request, 'account/home.html', {'vehicles': vehicles, 'equipment': equipment})

def is_admin(user):
    return user.is_authenticated and user.role == 'admin'

@login_required
def dashboard(request):
    total_vehicles = Vehicle.objects.count()
    total_equipment = Equipment.objects.count()
    total_blog_posts = BlogPost.objects.count()
    
    context = {
        'total_vehicles': total_vehicles,
        'total_equipment': total_equipment,
        'total_blog_posts': total_blog_posts,
    }
    return render(request, 'account/dashboard.html', context)

@login_required
def profile_view(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('account:dashboard')
    else:
        form = UserProfileForm(instance=request.user)
    
    base_template = 'account/admin_dashboard_base.html' if request.user.role == 'admin' else 'account/home.html'
    return render(request, 'account/profile.html', {
        'form': form,
        'base_template': base_template
    })

@user_passes_test(is_admin)
def manage_products(request):
    vehicles = Vehicle.objects.all()
    equipment = Equipment.objects.all()
    return render(request, 'account/manage_products.html', {
        'vehicles': vehicles,
        'equipment': equipment
    })

@user_passes_test(is_admin)
def product_create(request, product_type):
    if product_type == 'vehicle':
        form = VehicleForm(request.POST or None, request.FILES or None)
        model = Vehicle
    else:
        form = EquipmentForm(request.POST or None, request.FILES or None)
        model = Equipment

    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('account:manage_products')

    return render(request, 'account/product_form.html', {
        'form': form,
        'product_type': product_type,
        'action': 'Create'
    })

@user_passes_test(is_admin)
def product_update(request, product_type, pk):
    if product_type == 'vehicle':
        instance = get_object_or_404(Vehicle, pk=pk)
        form = VehicleForm(request.POST or None, request.FILES or None, instance=instance)
    else:
        instance = get_object_or_404(Equipment, pk=pk)
        form = EquipmentForm(request.POST or None, request.FILES or None, instance=instance)

    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('account:manage_products')

    return render(request, 'account/product_form.html', {
        'form': form,
        'product_type': product_type,
        'action': 'Update'
    })

@user_passes_test(is_admin)
def product_delete(request, product_type, pk):
    if product_type == 'vehicle':
        instance = get_object_or_404(Vehicle, pk=pk)
    else:
        instance = get_object_or_404(Equipment, pk=pk)
    
    if request.method == 'POST':
        instance.delete()
        return redirect('account:manage_products')
    
    return render(request, 'account/confirm_delete.html', {'item': instance})

@user_passes_test(is_admin)
def manage_blog(request):
    posts = BlogPost.objects.all()
    return render(request, 'account/manage_blog.html', {'posts': posts})

@user_passes_test(is_admin)
def blog_create(request):
    form = BlogPostForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect('account:manage_blog')
    return render(request, 'account/blog_form.html', {'form': form, 'action': 'Create'})

@user_passes_test(is_admin)
def blog_update(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    form = BlogPostForm(request.POST or None, request.FILES or None, instance=post)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('account:manage_blog')
    return render(request, 'account/blog_form.html', {'form': form, 'action': 'Update'})

@user_passes_test(is_admin)
def blog_delete(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    if request.method == 'POST':
        post.delete()
        return redirect('account:manage_blog')
    return render(request, 'account/confirm_delete.html', {'item': post})

def rent_vehicle(request):
    query = request.GET.get('q')
    category = request.GET.get('category')
    vehicles = Vehicle.objects.all()

    if category and category != 'all':
        vehicles = vehicles.filter(category=category)

    if query:
        vehicles = vehicles.filter(
            Q(name__icontains=query) | Q(category__icontains=query)
        )
    return render(request, 'account/rent_vehicle.html', {'vehicles': vehicles})

def rent_equipment(request):
    query = request.GET.get('q')
    category = request.GET.get('category')
    equipment = Equipment.objects.all()

    if category and category != 'all':
        equipment = equipment.filter(category=category)

    if query:
        equipment = equipment.filter(
            Q(name__icontains=query) | Q(category__icontains=query)
        )
    return render(request, 'account/rent_equipment.html', {'equipment': equipment})

def blog(request):
    posts = BlogPost.objects.all().order_by('-created_at')
    return render(request, 'account/blog.html', {'posts': posts})

def contact(request):
    return render(request, 'account/contact.html')



def product_detail(request, product_type, product_id):
    if product_type == 'vehicle':
        product = get_object_or_404(Vehicle, id=product_id)
    else:
        product = get_object_or_404(Equipment, id=product_id)
    
    context = {
        'product': product,
        'product_type': product_type
    }
    return render(request, 'account/product_detail.html', context)
