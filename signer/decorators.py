from functools import wraps

from django.contrib import messages
from django.shortcuts import redirect


def user_required(view_func):
    """Restrict view to regular users only."""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('user_login')
        if not hasattr(request.user, 'profile') or request.user.profile.is_authority:
            messages.error(request, 'Access denied. User account required.')
            return redirect('authority_dashboard' if request.user.profile.is_authority else 'user_login')
        return view_func(request, *args, **kwargs)
    return wrapper


def authority_required(view_func):
    """Restrict view to authority accounts only."""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('authority_login')
        if not hasattr(request.user, 'profile') or not request.user.profile.is_authority:
            messages.error(request, 'Access denied. Authority account required.')
            return redirect('dashboard' if hasattr(request.user, 'profile') else 'user_login')
        return view_func(request, *args, **kwargs)
    return wrapper
