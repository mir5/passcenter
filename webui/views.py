from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import deviceGroup,Device
from .forms import GroupForm


@login_required
def home(request):
    groups = deviceGroup.objects.all()
    devices = Device.objects.all()
    return render(request, 'webui/home.html', {'groups': groups, 'devices': devices})
@login_required
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
def group_update(request, pk):
    group = get_object_or_404(GroupForm, pk=pk)
    if request.method == 'POST':
        form = GroupForm(request.POST, instance=group)
        if form.is_valid():
            form.save()
            return redirect('group_list')
    else:
        form = GroupForm(instance=group)
    return render(request, 'webui/groups/group_form.html', {'form': form})
@login_required
def group_delete(request, pk):
    group = get_object_or_404(Group, pk=pk)
    if request.method == 'POST':
        group.delete()
        return redirect('group_list')
    return render(request, 'webui/groups/group_confirm_delete.html', {'group': group})
