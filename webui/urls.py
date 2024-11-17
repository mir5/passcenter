from django.urls import path
from . import views
from . import device_views
from .views import create_device_password,get_latest_password,custom_logout_view,list_device_passwords,change_password
from django.contrib.auth import views as auth_views

urlpatterns = [
    #home page
    path('', views.home, name='home'),
    
    
    path('groups/', views.group_list, name='group_list'),
    path('groups/new/', views.group_create, name='group_create'),
    path('groups/<int:pk>/edit/', views.group_update, name='group_update'),
    path('groups/<int:pk>/delete/', views.group_delete, name='group_delete'),
    
    
    # device urls
    path('devices/', device_views.device_list, name='device_list'), path('devices/new/', device_views.device_create, name='device_create'),
    path('devices/<int:pk>/edit/', device_views.device_update, name='device_update'),
    path('devices/<int:pk>/delete/', device_views.device_delete, name='device_delete'),
    path('create-device-password/<int:device_id>/', create_device_password, name='create_device_password'),
    path('get-latest-password/<int:device_id>/', get_latest_password, name='get_latest_password'),
    path('list-device-passwords/<int:device_id>/', list_device_passwords, name='list_device_passwords'),
    path('check-ssh-connectivity/', views.check_ssh_connectivity_view, name='check_ssh_connectivity'), 
    path('change-device-password/', views.change_device_password_view, name='change_device_password'),
    
    #auth system
    path('login/', auth_views.LoginView.as_view(template_name='webui/login.html'), name='login'), 
    path('logout/', custom_logout_view, name='custom_logout'),
    path('change-password/', change_password, name='change_password'), 
    
    
 

    # Other URL patterns...


    
]