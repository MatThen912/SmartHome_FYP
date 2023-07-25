from django import forms
from .models import *

class createdeviceForm(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Please enter the device name:"})
    )
    
    class Meta:
        model = Device
        fields = ['name', 'category']