#Session model stores the session data
from django.contrib.sessions.models import Session
from django.shortcuts import redirect
from django.urls import reverse_lazy
from accounts.models import LoggedInUser
from smartIOT.settings import LOGIN_URL

class OneSessionPerUserMiddleware:
    # Called only once when the web server starts
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        if request.user.is_authenticated:
            session_key = request.session.session_key

            try:
                logged_in_user = request.user.logged_in_user
                stored_session_key = logged_in_user.session_key
                # stored_session_key exists so delete it if it's different
                if stored_session_key != session_key:
                    Session.objects.filter(session_key=stored_session_key).delete()
                logged_in_user.session_key = session_key
                logged_in_user.save()
            except LoggedInUser.DoesNotExist:
                LoggedInUser.objects.create(user=request.user, session_key=session_key)

            stored_session_key = request.user.logged_in_user.session_key

            # if there is a stored_session_key  in our database and it is
            # different from the current session, delete the stored_session_key
            # session_key with from the Session table
            if stored_session_key and stored_session_key != request.session.session_key:
                Session.objects.get(session_key=stored_session_key).delete()

            request.user.logged_in_user.session_key = request.session.session_key
            request.user.logged_in_user.save()

        response = self.get_response(request)

        # This is where you add any extra code to be executed for each request/response after
        # the view is called.
        # For this tutorial, we're not adding any code so we just return the response

        return response

from smartIOT.settings import IGNORE_LOGIN_PATTERNS
import re 
class MustAuthenticatedMiddlware:
    # Called only once when the web server starts

    def __init__(self, get_response):
        self.get_response = get_response
        # self.reg = re.compile(IGNORE_LOGIN_PATTERNS)
        
        # Compile all the regex for performance gains
        self.regs = [re.compile(regex) for regex in IGNORE_LOGIN_PATTERNS]

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        response = self.get_response(request)
        
        for reg in self.regs:
            if reg.match(request.path_info):
                return response

        if not request.user.is_authenticated:

            if hasattr(request, 'exempt_authentication') and getattr(request, 'exempt_authentication'):
                return response 
            else:
                login_url = reverse_lazy('login')
                login_url = f"{login_url}?next={request.path_info if request.path_info else '/home'}"
                
                return redirect(login_url)
        # This is where you add any extra code to be executed for each request/response after
        # the view is called.
        # For this tutorial, we're not adding any code so we just return the response

        return response