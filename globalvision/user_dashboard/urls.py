from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_overview, name='user_dashboard'),
    path('profile/', views.user_profile, name='user_profile'),
    path('bookings/', views.user_bookings, name='user_bookings'),
    path('history/', views.user_history, name='user_history'),
    path('cart/', views.user_cart, name='user_cart'),
    path('support/', views.user_support, name='user_support'),
    path('logout/', views.user_logout, name='user_logout'),
    
    # Action endpoints
    path('bookings/<int:pk>/cancel/', views.cancel_booking, name='cancel_booking'),
    path('cart/<int:pk>/remove/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/checkout/', views.cart_checkout, name='cart_checkout'),
    path('cart/<int:pk>/update-dates/', views.update_cart_dates, name='update_cart_dates'),
]
