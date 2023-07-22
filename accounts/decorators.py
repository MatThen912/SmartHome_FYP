from functools import wraps
from http.client import HTTPResponse
from django.http import HttpResponseBadRequest
from django.http.response import HttpResponseForbidden
from django.contrib import messages
from django.shortcuts import redirect


def password_auth(view):
    """
    This decorator is used to authenticate request with password. So every incoming POST request must provide 
    password payload. the password will be then checked against current logged in user's password. 
    if it's true then the request will be forwarded to view function. else http forbidden will be retuned 
    """
    @wraps(view)
    def wrap(request, *args, **kwargs):
        if request.method != "POST":
            return  HttpResponseForbidden()
        
        password = request.POST.get('password')
        if not request.user.is_authenticated:
            messages.error('Must login')
            return HttpResponseForbidden()
        
        user = request.user 
        if not user.check_password(password):
            messages.error(request, 'password authentication failed')
            return redirect(request.META['HTTP_REFERER'])

        return view(request, *args, **kwargs)
    return wrap 

def login_exempt(view):
    """
    Used to exempt view from login required middleware
    """
    @wraps(view)
    def wrap(request, *args, **kwargs):
        request.exempt_authentication = True
        return view(request, *args, **kwargs)
    return wrap 