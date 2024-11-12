from django import forms
from .models import deviceGroup,Device,DevicePassword
from .validators import validate_ip_address
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

from django.contrib.auth.forms import PasswordChangeForm

class GroupForm(forms.ModelForm):
    admins = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(), 
        widget=forms.CheckboxSelectMultiple,
        required=False, label='Admins' )
    class Meta:
        model = deviceGroup
        fields = ['name', 'description','admins', 'status']
        
        

class DeviceForm(forms.ModelForm):
    class Meta:
        model = Device 
        fields = ['group', 'name', 'ip', 'domain_name', 'status', 'remote_user', 'remote_password', 'access_protocol'] 
        widgets = { 
                   'group': forms.Select(attrs={'class': 'form-control'}), 
                   'name': forms.TextInput(attrs={'class': 'form-control'}), 
                   'ip': forms.TextInput(attrs={'class': 'form-control'}), 
                   'domain_name': forms.TextInput(attrs={'class': 'form-control'}), 
                   'status': forms.CheckboxInput(attrs={'class': 'form-check-input'}), 
                   'remote_user': forms.TextInput(attrs={'class': 'form-control'}), 
                   'remote_password': forms.PasswordInput(attrs={'class': 'form-control'}), 
                   'access_protocol': forms.Select(attrs={'class': 'form-control'}),
                }
        def clean_ip(self):
            ip = self.cleaned_data.get('ip')
            validate_ip_address(ip)
            return ip





class DevicePasswordForm(forms.ModelForm):
    class Meta:
        model = DevicePassword
        fields = ['description', 'valid_time']
        widgets = {
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'valid_time': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
        }
        

class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label="Old Password"
    )
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label="New Password"
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label="Confirm New Password"
    )




