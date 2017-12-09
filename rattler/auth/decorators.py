from functools import wraps
from django.utils.decorators import available_attrs
from django.shortcuts import resolve_url, redirect

def not_login_required(function=None, redirect_to=None):
    """
    Decorator for views that checks that the user is not logged in, redirecting
    to the redirect to page if necessary.
    """
    @wraps(function, assigned=available_attrs(function))
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return function(request, *args, **kwargs)
        resolved_url = resolve_url(redirect_to or '/')
        return redirect(resolved_url)
    return _wrapped_view
