from functools import wraps
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.urls import reverse
 
def admin_required(view):
    """
        decorator for views. redirect on homepage if the user is not logged and user is not admin
    """
    @wraps(view)
    def _view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(reverse('homepage'))
        if not request.user.is_superuser:
            return redirect(reverse('homepage'))
        return view(request, *args, **kwargs)
    return _view
 