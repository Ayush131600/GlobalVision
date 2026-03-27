from django.urls import path
from .views import (
    login, admin_login, register, logout_view, rent_vehicle, rent_equipment, blog, contact, about, product_detail,
    profile_view, manage_products, product_create, product_update, product_delete,
    manage_blog, blog_create, blog_update, blog_delete,
    password_reset_request, password_reset_verify, password_reset_set_new
)

app_name = 'account'

urlpatterns = [
    path('login/', login, name="login"),
    path('admin-login/', admin_login, name="admin_login"),
    path('register/', register, name="register"),
    path('logout/', logout_view, name="logout"),
    path('rent/vehicle/', rent_vehicle, name="rent_vehicle"),
    path('rent/equipment/', rent_equipment, name="rent_equipment"),
    path('blog/', blog, name="blog"),
    path('contact/', contact, name="contact"),
    path('about/', about, name="about"),
    path('product/<str:product_type>/<int:product_id>/', product_detail, name="product_detail"),
    
    # Dashboard & Management
    path('profile/', profile_view, name="profile"),
    path('manage/products/', manage_products, name="manage_products"),
    path('manage/products/create/<str:product_type>/', product_create, name="product_create"),
    path('manage/products/update/<str:product_type>/<int:pk>/', product_update, name="product_update"),
    path('manage/products/delete/<str:product_type>/<int:pk>/', product_delete, name="product_delete"),
    path('manage/blog/', manage_blog, name="manage_blog"),
    path('manage/blog/create/', blog_create, name="blog_create"),
    path('manage/blog/update/<int:pk>/', blog_update, name="blog_update"),
    
    # Custom OTP Password Reset
    path('password-reset/', 
         password_reset_request, 
         name='password_reset'),
    path('password-reset/verify/', 
         password_reset_verify, 
         name='password_reset_verify'),
    path('password-reset/confirm/', 
         password_reset_set_new, 
         name='password_reset_set_new'),
]
