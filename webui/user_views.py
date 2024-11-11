from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .forms import CustomUserForm

User = get_user_model()

@login_required
def create_user(request):
    if request.method == 'POST':
        form = CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_list')
    else:
        form = CustomUserForm()
    return render(request, 'webui/user_form.html', {'form': form})

@login_required
def delete_user(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    user.delete()
    return redirect('user_list')

@login_required
def disable_user(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    user.is_active = False
    user.save()
    return redirect('user_list')

@login_required
def modify_password(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        user.set_password(new_password)
        user.save()
        return redirect('user_list')
    return render(request, 'webui/modify_password.html', {'user': user})
