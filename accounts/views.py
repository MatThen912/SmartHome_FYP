import traceback
from typing import Any
from django.db.models import Prefetch
from datetime import timedelta
import datetime
import mimetypes
import os
from django_user_agents.utils import get_user_agent
from django_user_agents.utils import parse
from django.http import HttpRequest, JsonResponse
from django.urls import reverse_lazy
import pandas as pd
from django.http.response import HttpResponse
from accounts.decorators import login_exempt
from accounts.models import Account
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from accounts.forms import *
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login as auth_login, authenticate
from django.contrib.auth.models import User, auth, Group
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm
from django.views.generic import (
    ListView,

)
from smartIOT.settings import DEBUG, SESSION_COOKIE_AGE
from .models import Account,Userlog
from django.contrib.auth.models import Permission
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.core.mail import send_mail, BadHeaderError
import pandas as pd
from django.views import View
from django.utils.decorators import method_decorator
from device import urls



class LoginView(View):
    @method_decorator(login_exempt)
    def post(self, request, *args, **kwargs):
        login_form = loginForm(data=request.POST)

        next_url = request.POST.get(
            'next_url') if 'next_url' in request.POST else reverse_lazy('dashboard')
        if login_form.is_valid():
            user = login_form.get_user()
            auth_login(request, user)
            ip = get_client_ip(request)
            device = get_userdevive(request)
            time = get_time(request)
            userlog = Userlog(
                user=user,
                ip=ip,
                device=device,
                last_activation_date=time,
            )
            userlog.save()
            remember_me = login_form.cleaned_data["remember_me"]
            if remember_me:
                # print(remember_me)
                request.session.set_expiry(1209600)

        # print(request.user.is_authenticated) # testing
            return redirect(next_url)
        else:
            next_url = request.POST.get(
            'next_url') if 'next_url' in request.POST else reverse_lazy('home')

            login_form = loginForm()
            context = {
                'next_url': next_url,
                'login_form': login_form,
                "errors": login_form.errors,
            }
            messages.warning(request, 'Invalid username or password!')

            return render(request, "accounts/login.html", context=context)

    @method_decorator(login_exempt)
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('dashboard')
        login_form = loginForm()

        next_url = request.GET.get(
            'next') if 'next' in request.GET else reverse_lazy('dashboard')

        context = {
            'login_form': login_form,
            'next_url': next_url
        }
        return render(request, "accounts/login.html", context=context)



def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        # If 'HTTP_X_FORWARDED_FOR' header exists, it may contain a comma-separated list of IPs.
        # We split it and take the first IP as the client's real IP address.
        ip = x_forwarded_for.split(',')[0]
    else:
        # If 'HTTP_X_FORWARDED_FOR' is not present, we fall back to 'REMOTE_ADDR'.
        # This should give us the client's IP address directly.
        ip = request.META.get('REMOTE_ADDR', 'UNKNOWN')  # Provide a default value in case 'REMOTE_ADDR' is missing.

    return ip

def get_userdevive(request):
    user_agent = parse(request.META['HTTP_USER_AGENT'])
    device_type = user_agent.device.family  # e.g., 'iPhone', 'Android', 'Desktop', etc.
    browser_family = user_agent.browser.family  # e.g., 'Chrome', 'Firefox', 'Safari', etc.
    browser_version = user_agent.browser.version_string
    os_family = user_agent.os.family
    os_version = user_agent.os.version_string 

    device =browser_family+' '+browser_version+' on '+os_family+' in '+device_type
    return device

def get_time(request):
    time = datetime.datetime.now()
    return time.strftime('%Y-%m-%d %H:%M:%S')

@login_exempt
def logout(request):
    auth.logout(request)
    return redirect("login")


@login_exempt
def permission_denied(request):
    return render(request, "accounts/errorpage.html")


def temporary_home(request):
    return render(request, "accounts/temporary_home.html")

   
  

def get_user_permissions(user):
    if user.is_superuser:
        return Permission.objects.all()
    return user.user_permissions.all() | Permission.objects.filter(group__user=user)


class AddUserView(View, LoginRequiredMixin, PermissionRequiredMixin):
    permission_required = 'accounts.add_account'
    raise_exception = True

    def get(self, request, *args, **kwargs):
        obj_query = Account.objects.filter(role=request.GET.get("id_role"))
        if len(obj_query) > 0:
            obj = obj_query[0]
            data = get_user_permissions(obj)
            form = createUserForm(
                initial={"role": request.GET.get("role"), "permissions": data}
            )
        else:
            form = createUserForm(initial={"role": request.GET.get("role")})
        context = {
            "form": form,
        }
        return render(request, "accounts/userCreation.html", context)

    def post(self, request, *args, **kwargs):
        form = createUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            form.save_m2m()
            user.save()
            messages.success(request, "User created successfully!")
            return redirect("userlist")
        else:
            messages.warning(request,  form.errors)
            
            context = {
                "errors": form.errors,
                "form": form,
            }
            return render(request, "accounts/userCreation.html", context)






class ViewUserView(View, LoginRequiredMixin, PermissionRequiredMixin):
    permission_required = 'accounts.view_account'
    raise_exception = True

    def post(self, request, pk, *args, **kwargs):
        user = Account.objects.get(account_id=pk)
        return redirect("userlist")

    def get(self, request, pk, *args, **kwargs):
        user = Account.objects.get(account_id=pk)
        user1 = Account.objects.filter(account_id=pk)
        form = viewUserForm(instance=user)
        profile_pic = user.profile_pic
        context = {
            "profile_pic":profile_pic,
            "form": form,
            "pk": pk,
            'user':user1
        }
        return render(request, "accounts/profile.html", context)


class EditUserView(View, LoginRequiredMixin, PermissionRequiredMixin):
    permission_required = 'accounts.change_account'
    raise_exception = True

    def post(self, request, pk, *args, **kwargs):
        user = Account.objects.get(account_id=pk)
        currRole =request.user.role
        if(currRole == 'Super Admin' ):
            form = AdmineditUserForm(request.POST, instance=user)
        else:
            form = editUserForm(request.POST, instance=user)
        owner = (request.user.account_id == pk)
        if form.is_valid():
            user = form.save()
            permissions = request.POST.getlist('permissions')
            role = request.POST.get("role")


            user.save()
            messages.success(request, "Successfully updated profile!")

            if(owner and (role == "Supervisor" or role == "Operator" or role == "External Vet")):
                return redirect('logout')

            return redirect(f'/viewUser/{user.account_id}')
        else:
            extra_context = {
                "form": form,
                "errors": form.errors,
                "is_user": (request.user.account_id == user.account_id),
            }
            print('something wrong')
            messages.error(request, "Invalid input! Please input a valid information.")
            return render(request, "accounts/editUser.html", extra_context)

    def get(self, request, pk, *args, **kwargs):
        user = Account.objects.get(account_id=pk)
        loguser = Account.objects.get(account_id=pk)
        currRole =request.user.role
        if(currRole == 'Super Admin' ):
            form = AdmineditUserForm(instance=user)
        else:
            form =  editUserForm(instance=user)
        print(user.password)
        print(request.user.role)
        extra_context = {
            "form": form,
            "is_user": (request.user.account_id == user.account_id),
            "role": currRole,
        }
        return render(request, "accounts/editUser.html", extra_context)


class UpdateProfilePicView(View, LoginRequiredMixin, PermissionRequiredMixin):
    permission_required = 'accounts.change_account'
    raise_exception = True

    def post(self, request, pk, *args, **kwargs):
        user = Account.objects.get(account_id=pk)
        user.profile_pic = request.FILES.get('profile-pic')
        user.save()
        return redirect('viewUser', pk)



@permission_required('accounts.delete_account', raise_exception=True)
def deleteUser(request, event_id):
    print(event_id)
    event = Account.objects.get(pk=event_id)
    event.delete()
    messages.success(request, "User deleted successfully!")
    return redirect('userlist')


class UserListView(LoginRequiredMixin,ListView):

    template_name = "accounts/user_list.html"
    queryset = Account.objects.all()



def get_viewUser(request, username):
    username = User.objects.get(username=username)
    return render(request, "accounts/user_list.html", {"user": User})


class ResetPasswordView(View, LoginRequiredMixin, PermissionRequiredMixin):
    permission_required = 'accounts.change_account'
    raise_exception = True

    @method_decorator(login_exempt)
    def post(self, request, *args, **kwargs):
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data["email"]
            associated_users = Account.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "password/password_reset_email.txt"
                    c = {
                            "email": user.email,
                            "domain": "127.0.0.1:8000",  # soon need to change this to production domain
                            "site_name": "CCB Website",
                            "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                            "user": user,
                            "token": default_token_generator.make_token(user),
                            "protocol": "http",  # https when is production
                    }
                    email = render_to_string(email_template_name, c)

                    try:
                        # example of email
                        send_mail(
                            subject,
                            email,
                            "admin@mail.com",
                            [user.email],
                            fail_silently=False,
                        )
                    except BadHeaderError:
                        return HttpResponse("Invalid header found")

                    messages.success(
                        request,
                        "A message with reset password instructions has been sent to your inbox.",
                    )
                    return redirect("/password_reset/done/")
            else:
                messages.warning(request, "An invalid email has been entered.")

        password_reset_form = PasswordResetForm()
        return render(
            request,
            template_name="password/password_reset.html",
            context={"password_reset_form": password_reset_form},
        )

    @method_decorator(login_exempt)
    def get(self, request, *args, **kwargs):
        password_reset_form = PasswordResetForm()
        return render(
            request,
            template_name="password/password_reset.html",
            context={"password_reset_form": password_reset_form},
        )


@login_exempt
def in_progress(request):
    return render(request, "accounts/in_progress.html")


@login_exempt
def no_permission_page(request):
    return render(request, "accounts/no_permission_page.html")




# ADD DECORATORS TO DJANGO DEFAUL AUTH VIEWS
from django.contrib.auth import views as auth_views

class PasswordResetDoneView(auth_views.PasswordResetDoneView):
    @method_decorator(login_exempt)
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

class PasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    @method_decorator(login_exempt)
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    @method_decorator(login_exempt)
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        return super().get(request, *args, **kwargs)

class PasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    @method_decorator(login_exempt)
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        return super().get(request, *args, **kwargs)
