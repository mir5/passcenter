from django.urls import path
from . import views
from . import device_views,user_views
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
    
    
    #auth system
    path('login/', auth_views.LoginView.as_view(template_name='webui/login.html'), name='login'), 
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    
    #user managment

    path('create-user/', user_views.create_user, name='create_user'),
    path('delete-user/<int:user_id>/', user_views.delete_user, name='delete_user'),
    path('disable-user/<int:user_id>/', user_views.disable_user, name='disable_user'),
    path('modify-password/<int:user_id>/', user_views.modify_password, name='modify_password'),
    # Other URL patterns...


    
]