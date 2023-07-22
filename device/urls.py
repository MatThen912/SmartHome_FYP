from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.views.decorators.cache import cache_page


urlpatterns = [
    path("dashboard", views.deviceDashboardview, name="dashboard"),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)