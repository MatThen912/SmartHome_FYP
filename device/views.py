from django.views.generic import (
View
)
from django.shortcuts import render
import pandas as pd
from accounts.models import Userlog


def deviceDashboardview(request):
    return render(request, "devicedashboard.html")

