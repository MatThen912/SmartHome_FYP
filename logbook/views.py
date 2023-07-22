
from django.views.generic import (
View
)
from django.shortcuts import render
import pandas as pd
from accounts.models import Userlog

def  userlogview(request):
    userlog = Userlog.objects.all()
    context = {
        'userlog':userlog
    }
    return render(request, 'userlog.html', context)