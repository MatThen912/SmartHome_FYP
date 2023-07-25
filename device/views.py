from django.views.generic import (
View
)
from django.shortcuts import render,redirect
import pandas as pd
from accounts.models import Userlog
import json
from django.shortcuts import get_object_or_404
from django.http import JsonResponse, HttpResponse 
from devices.models import Device
from devices.forms import createdeviceForm
from django.contrib import messages


def deviceDashboardview(request):
    device = Device.objects.all()
    context = {
        'devicelist':device
    }
    return render(request, "devicedashboard.html",context)

def toggle_device(request, device_id):
    try:
        device = Device.objects.get(device_id=device_id)
        device.status = not device.status  # Toggle the status
        device.save()
        print("true")
        return JsonResponse({'status': device.status})
    except Device.DoesNotExist:
        return JsonResponse({'error': 'Device not found'}, status=404)
    
def add_device(request):
    if request.method == 'POST':
        form = createdeviceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')  # Assuming you have a view named 'device_list' to display all devices
    else:
        form = createdeviceForm()
    return render(request, 'adddevice.html', {'form': form})

def devicelistview(request):
    device = Device.objects.all()
    currRole =request.user.role
    context = {
        'devicelist':device,
        'role':currRole
    }
    return render(request, 'devicelist.html', context)

def delete_device(request,device_id):
    print(device_id)
    event = Device.objects.get(pk=device_id)
    event.delete()
    messages.success(request, "User deleted successfully!")
    return redirect('devicelist')