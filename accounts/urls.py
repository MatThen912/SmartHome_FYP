from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.views.decorators.cache import cache_page


urlpatterns = [
    path("home", views.temporary_home, name="home"),
    path("addUser",views.AddUserView.as_view(), name="addUser"),
    path("", views.LoginView.as_view(), name="login"),
    path("logout", views.logout, name="logout"),
    path("errorpage", views.permission_denied, name="errorpage"),
    path("userlist", views.UserListView.as_view(), name="userlist"),
    path("forgot-password/", views.ResetPasswordView.as_view(), name="forgot-password"),
    path("viewUser/<uuid:pk>/", views.ViewUserView.as_view(), name="viewUser"),
    path("editUser/<uuid:pk>/", views.EditUserView.as_view(), name="editUser"),
    path("deleteUser/<event_id>/", views.deleteUser, name="deleteUser"),
    path("updateProfilePic/<uuid:pk>/", views.UpdateProfilePicView.as_view(), name="updateProfilePic"),
    path("in_progress", views.in_progress, name="in_progress"),
    path("no_permission_page", views.no_permission_page, name="no_permission_page"),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
