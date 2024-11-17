from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth import logout
from .models import deviceGroup,Device,DevicePassword
from .forms import GroupForm
from .forms import DevicePasswordForm
from django.shortcuts import render, redirect
from django.contrib.auth import update_session_auth_hash
from .forms import CustomPasswordChangeForm
import random
import string
from django.http import JsonResponse
import json

def staff_user_required(user):
    return user.is_authenticated and user.is_staff

@login_required
def home(request):
    user=request.user
    
    if not request.user.is_superuser:
        groups = deviceGroup.objects.filter(admins=user).distinct()
        devices = Device.objects.filter(group__admins=user).distinct()
    else:
        groups = deviceGroup.objects.all()
        devices = Device.objects.all()
        
   
    return render(request, 'webui/home.html', {'groups': groups, 'devices': devices})
@login_required
@user_passes_test(staff_user_required)
def group_list(request):
    groups = deviceGroup.objects.all()
    filter_status = request.GET.get('status')
    sort_by = request.GET.get('sort_by')
    if filter_status:
        groups = groups.filter(status=(filter_status == 'active'))
    if sort_by:
        groups = groups.order_by(sort_by)
    return render(request, 'webui/groups/group_list.html', {'groups': groups})
@login_required
@user_passes_test(staff_user_required)
def group_create(request):
    if request.method == 'POST':
        form = GroupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('group_list')
    else:
        form = GroupForm()
    return render(request, 'webui/groups/group_form.html', {'form': form})
@login_required
@user_passes_test(staff_user_required)
def group_update(request, pk):
    group = get_object_or_404(deviceGroup, pk=pk)
    if request.method == 'POST':
        form = GroupForm(request.POST, instance=group)
        if form.is_valid():
            form.save()
            return redirect('group_list')
    else:
        form = GroupForm(instance=group)
    return render(request, 'webui/groups/group_form.html', {'form': form})
@login_required
@user_passes_test(staff_user_required)
def group_delete(request, pk):
    group = get_object_or_404(deviceGroup, pk=pk)
    if request.method == 'POST':
        group.delete()
        return redirect('group_list')
    return render(request, 'webui/groups/group_confirm_delete.html', {'group': group})




@login_required
def create_device_password(request, device_id):
    device = get_object_or_404(Device, id=device_id)

    if request.method == 'POST':
        form = DevicePasswordForm(request.POST)
        if form.is_valid():
            # Update the DevicePassword instances for the current user and device
            DevicePassword.objects.filter(device=device, user=request.user).update(status=False)

            device_password = form.save(commit=False)
            device_password.device = device
            device_password.user = request.user
            device_password.username = request.user.username
            device_password.password = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
            device_password.status = True
            device_password.save()
            return redirect('home')  # Redirect to home or another relevant page
    else:
        form = DevicePasswordForm()

    return render(request, 'webui/devices/create_device_password.html', {'form': form, 'device': device})


from django.http import JsonResponse

@login_required

def get_latest_password(request, device_id):
    
    user=request.user
    device = get_object_or_404(Device, id=device_id)
    latest_password = DevicePassword.objects.filter(device=device, status=True,user = user).order_by('-valid_time').first()

    if latest_password:
        message = f"Latest Password: {latest_password.password}"
    else:
        message = "Please use the action button to get a new password"

    return JsonResponse({'message': message})


def custom_logout_view(request):
    logout(request)
    return redirect('/ui/login')




from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Device, DevicePassword
from django.contrib.auth.models import User

@login_required
@user_passes_test(staff_user_required)
def list_device_passwords(request, device_id):
    device = get_object_or_404(Device, id=device_id)
    passwords = DevicePassword.objects.filter(device=device).order_by('-valid_time')
    
    

    return render(request, 'webui/devices/list_device_passwords.html', {
        'device': device,
        'passwords': passwords,
       
    })



@login_required
def change_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important to keep the user logged in
            return redirect('webui/users/password_change_done')
    else:
        form = CustomPasswordChangeForm(request.user)

    return render(request, 'webui/users/change_password.html', {'form': form})



import paramiko
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

def check_ssh_connectivity(device):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(device.ip, port=device.port, username=device.remote_user, password=device.remote_password)
        client.close()
        return "OK"
    except Exception as e:
        return f"Error: {str(e)}"

@csrf_exempt
@login_required
@user_passes_test(staff_user_required)
def check_ssh_connectivity_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        device_ids = data.get('device_ids', [])
        response_data = {}

        for device_id in device_ids:
            device = get_object_or_404(Device, id=device_id)
            response_data[device_id] = check_ssh_connectivity(device)
        
        return JsonResponse(response_data)

    return JsonResponse({'error': 'Invalid request'}, status=400)

import json
import paramiko
import random
import string
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404
from .models import Device

def generate_random_password(length=20): 
    characters = string.ascii_letters + string.digits # Only alphabets and numbers 
    return ''.join(random.choice(characters) for _ in range(length))

def change_device_password(device, new_password):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(device.ip, port=device.port, username=device.remote_user, password=device.remote_password)
        # Use 'sudo passwd' command without password prompt
        command = f'echo -e "{new_password}\\n{new_password}" | sudo /usr/bin/passwd {device.remote_user}'
        print(command)
        stdin, stdout, stderr = client.exec_command(command)
        stdout.channel.recv_exit_status()  # Ensure the command completes
        client.close()
        return "OK"
    except Exception as e:
        return f"Error: {str(e)}"

@csrf_exempt
@login_required
@user_passes_test(staff_user_required)
def change_device_password_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            device_ids = data.get('device_ids', [])
            response_data = {}

            for device_id in device_ids:
                device = get_object_or_404(Device, id=device_id)
                new_password = generate_random_password()
                ssh_status = change_device_password(device, new_password)

                if ssh_status == "OK":
                    device.remote_password = new_password
                    device.save()
                response_data[device_id] = ssh_status

            return JsonResponse(response_data)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

    return JsonResponse({'error': 'Invalid request'}, status=400)
