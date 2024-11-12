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
@user_passes_test(staff_user_required)
def create_device_password(request, device_id):
    device = get_object_or_404(Device, id=device_id)

    if request.method == 'POST':
        form = DevicePasswordForm(request.POST)
        if form.is_valid():
            DevicePassword.objects.filter(device=device).update(status=False)
            device_password = form.save(commit=False)
            device_password.device = device
            device_password.user = request.user
            device_password.username=request.user.username
            device_password.password = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
            device_password.status = True
            device_password.save()
            return redirect('home')  # Redirect to home or another relevant page
    else:
        form = DevicePasswordForm()

    return render(request, 'webui/devices/create_device_password.html', {'form': form, 'device': device})


from django.http import JsonResponse

@login_required
@user_passes_test(staff_user_required)
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




@login_required

def list_device_passwords(request, device_id):
    device = get_object_or_404(Device, id=device_id)
    passwords = DevicePassword.objects.filter(device=device).order_by('-valid_time')

    return render(request, 'webui/devices/list_device_passwords.html', {
        'device': device,
        'passwords': passwords
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



