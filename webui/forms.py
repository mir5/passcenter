from django import forms
from .models import deviceGroup,Device
from .validators import validate_ip_address
from django.contrib.auth import get_user_model

class GroupForm(forms.ModelForm):
    class Meta:
        model = deviceGroup
        fields = ['name', 'description', 'status']
        
        

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




class CustomUserForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['username', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            # 'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            # 'user_level': forms.NumberInput(attrs={'class': 'form-control'}),
            # 'status': forms.NumberInput(attrs={'class': 'form-control'}),
            # 'admin': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


