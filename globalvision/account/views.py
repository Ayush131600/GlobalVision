from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Q
from .models import User
from inventory.models import Vehicle, Equipment, Review
from inventory.forms import ReviewForm
from blog.models import BlogPost
from contacts.models import ContactMessage
from cms.models import AboutPage, SiteSettings, TeamMember
from bookings.models import Booking, get_unavailable_dates
from django.contrib.contenttypes.models import ContentType
# from dashboard.forms import VehicleForm, EquipmentForm, BlogPostForm
from .forms import UserProfileForm
from functools import wraps


def login(request):
    if request.user.is_authenticated:
        next_url = request.GET.get('next') or request.POST.get('next')
        if next_url:
            return redirect(next_url)
        if request.user.role == 'admin' or request.user.is_staff:
            return redirect('admin:index')
        return redirect('home')
        
    if request.method == "POST":
        login_input = request.POST.get("user_name")
        password = request.POST.get("password")

        # Try to find user by email first
        user_to_auth = login_input
        if "@" in login_input:
            user_obj = User.objects.filter(email__iexact=login_input).first()
            if user_obj:
                user_to_auth = user_obj.user_name

        # Authenticate using standard 'username' keyword (Django maps this to USERNAME_FIELD)
        user = authenticate(request, username=user_to_auth, password=password)
        
        # Fallback to 'user_name' keyword if 'username' fails
        if user is None:
            user = authenticate(request, user_name=user_to_auth, password=password)

        if user is not None:
            auth_login(request, user)
            next_url = request.GET.get('next') or request.POST.get('next')
            if next_url:
                return redirect(next_url)
            if user.role == 'admin' or user.is_staff:
                return redirect('admin:index')
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

        # Try both 'username' and 'user_name' keywords
        user = authenticate(request, username=user_name, password=password)
        if user is None:
            user = authenticate(request, user_name=user_name, password=password)

        if user is not None and user.role == 'admin':
            auth_login(request, user)
            return redirect("admin:index")
        else:
            messages.error(
                request,
                "Invalid admin credentials or unauthorized access",
                extra_tags="error"
            )

    return render(request, "account/admin_login.html")





def register(request):
    if request.user.is_authenticated:
        return redirect('home')

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
            return redirect("account:register")

        if User.objects.filter(user_name=user_name).exists():
            messages.error(
                request,
                "Username already exists",
                extra_tags="error"
            )
            return redirect("account:register")

        if User.objects.filter(email=email).exists():
            messages.error(
                request,
                "Email already exists",
                extra_tags="error"
            )
            return redirect("account:register")

        if not phone_no.isdigit():
            messages.error(
                request,
                "Phone number must contain only digits",
                extra_tags="error"
            )
            return redirect("account:register")

        if not (10 <= len(phone_no) <= 15):
            messages.error(
                request,
                "Phone number should be between 10 and 15 digits",
                extra_tags="error"
            )
            return redirect("account:register")

        if User.objects.filter(phone_no=phone_no).exists():
            messages.error(
                request,
                "Phone number already exists",
                extra_tags="error"
            )
            return redirect("account:register")

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
def profile_view(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "User details successfully updated.", extra_tags="success")
            return redirect('account:profile')
    else:
        form = UserProfileForm(instance=request.user)
    
    base_template = 'account/base.html'
    return render(request, 'account/profile.html', {
        'form': form,
        'base_template': base_template
    })

@user_passes_test(is_admin)
def manage_products(request):
    vehicles = Vehicle.objects.all()
    equipment = Equipment.objects.all()
    return render(request, 'inventory/manage_products.html', {
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

    return render(request, 'inventory/product_form.html', {
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

    return render(request, 'inventory/product_form.html', {
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
    
    return render(request, 'inventory/confirm_delete.html', {'item': instance})

@user_passes_test(is_admin)
def manage_blog(request):
    posts = BlogPost.objects.all()
    return render(request, 'blog/manage_blog.html', {'posts': posts})


@user_passes_test(is_admin)
def blog_create(request):
    form = BlogPostForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect('account:manage_blog')
    return render(request, 'blog/blog_form.html', {'form': form, 'action': 'Create'})

@user_passes_test(is_admin)
def blog_update(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    form = BlogPostForm(request.POST or None, request.FILES or None, instance=post)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('account:manage_blog')
    return render(request, 'blog/blog_form.html', {'form': form, 'action': 'Update'})

@user_passes_test(is_admin)
def blog_delete(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    if request.method == 'POST':
        post.delete()
        return redirect('account:manage_blog')
    return render(request, 'inventory/confirm_delete.html', {'item': post})

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
    return render(request, 'inventory/rent_vehicle.html', {'vehicles': vehicles})


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
    return render(request, 'inventory/rent_equipment.html', {'equipment': equipment})


def blog(request):
    posts = BlogPost.objects.filter(is_published=True).order_by('-created_at')
    return render(request, 'blog/blog.html', {'posts': posts})


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message_content = request.POST.get('message')
        
        if name and email and message_content:
            ContactMessage.objects.create(
                user=request.user if request.user.is_authenticated else None,
                name=name,
                email=email,
                subject=subject or 'No Subject',
                message=message_content
            )
            print(f"DEBUG: Message saved from {name}")
            messages.success(request, 'Thank you! Your message has been sent to our team.')
            return redirect('account:contact')
            
    settings = SiteSettings.objects.first()
    return render(request, 'contacts/contact.html', {'settings': settings})


def about(request):
    return render(request, 'cms/about.html')




def product_detail(request, product_type, product_id):
    if product_type == 'vehicle':
        product = get_object_or_404(Vehicle, id=product_id)
    else:
        product = get_object_or_404(Equipment, id=product_id)
    
    unavailable_dates = get_unavailable_dates(product)
    
    # Fetch reviews
    content_type = ContentType.objects.get_for_model(product)
    reviews = Review.objects.filter(content_type=content_type, object_id=product.id)
    review_form = ReviewForm()
    
    context = {
        'product': product,
        'product_type': product_type,
        'unavailable_dates': unavailable_dates,
        'reviews': reviews,
        'review_form': review_form
    }
    return render(request, 'inventory/product_detail.html', context)


import random
from django.core.mail import send_mail
from django.conf import settings
from .models import PasswordResetOTP

def password_reset_request(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        user = User.objects.filter(email__iexact=email).first()
        
        if user:
            # Generate 6-digit OTP
            otp = str(random.randint(100000, 999999))
            
            # Save OTP to database
            PasswordResetOTP.objects.create(email=email, otp_code=otp)
            
            # Send Email
            subject = 'Password Reset Verification Code'
            message = f'Your verification code for password reset is: {otp}. It will expire in 10 minutes.'
            email_from = settings.DEFAULT_FROM_EMAIL
            recipient_list = [email]
            send_mail(subject, message, email_from, recipient_list)
            
            # Store email in session for the next step
            request.session['reset_email'] = email
            messages.success(request, "Verification code sent to your email.")
            return redirect('account:password_reset_verify')
        else:
            messages.error(request, "No account found with this email.")
            
    return render(request, 'account/password_reset_form.html')

def password_reset_verify(request):
    email = request.session.get('reset_email')
    if not email:
        return redirect('account:password_reset_request')
        
    if request.method == 'POST':
        otp_entered = request.POST.get('otp')
        otp_obj = PasswordResetOTP.objects.filter(email=email, otp_code=otp_entered, is_used=False).last()
        
        if otp_obj and not otp_obj.is_expired():
            otp_obj.is_used = True
            otp_obj.save()
            request.session['otp_verified'] = True
            return redirect('account:password_reset_set_new')
        else:
            messages.error(request, "Invalid or expired verification code.")
            
    return render(request, 'account/password_reset_verify.html', {'email': email})

def password_reset_set_new(request):
    email = request.session.get('reset_email')
    verified = request.session.get('otp_verified')
    
    if not email or not verified:
        return redirect('account:password_reset_request')
        
    if request.method == 'POST':
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        if password and password == confirm_password:
            user = User.objects.filter(email=email).first()
            if user:
                user.set_password(password)
                user.save()
                
                # Clear session
                del request.session['reset_email']
                del request.session['otp_verified']
                
                messages.success(request, f"Password reset successful for {user.user_name}. You can now login.")
                return redirect('account:login')
            else:
                messages.error(request, "User not found.")
                return redirect('account:password_reset_request')
        else:
            messages.error(request, "Passwords do not match or are empty.")
            
    return render(request, 'account/password_reset_confirm.html')
