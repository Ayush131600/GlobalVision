from django.shortcuts import redirect
from functools import wraps
from django.contrib import messages

def user_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.info(request, "Please login to access your dashboard.")
            return redirect('account:login')
            
        return view_func(request, *args, **kwargs)
            
        return view_func(request, *args, **kwargs)
    return _wrapped_view
