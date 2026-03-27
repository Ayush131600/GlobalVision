from django.shortcuts import redirect
from functools import wraps
from django.contrib import messages

def user_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.info(request, "Please login to access your dashboard.")
            return redirect('account:login')
        
        if request.user.role == 'admin' or request.user.is_staff:
            return redirect('dashboard_home')
        
        if request.user.role != 'user':
            messages.error(request, "Access denied. Customers only.")
            return redirect('home')
            
        return view_func(request, *args, **kwargs)
    return _wrapped_view
