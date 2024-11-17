from django.db import models
from django.contrib.auth.models import AbstractUser,User,BaseUserManager

class deviceGroup(models.Model):
    name = models.CharField(max_length=255)
    icon = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    admins = models.ManyToManyField(User, related_name='admin_groups')
    status = models.BooleanField() 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name


class Device(models.Model):
    SSH='ssh'
    TELNET="telnet"
    RDP="RDP"
    ACCESS_PROTOCOL_CHOICES=[
        (SSH,'SSH'),
        (TELNET,'TELNET'),
        (RDP,'RDP')
    ]
    group = models.ForeignKey(deviceGroup, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    ip = models.GenericIPAddressField()
    port= models.IntegerField(default=22)
    domain_name = models.CharField(max_length=255, null=True, blank=True)
    status = models.BooleanField()
    remote_user = models.CharField(max_length=255)
    remote_password = models.CharField(max_length=255)
    access_protocol = models.CharField(max_length=10,
                                       choices=ACCESS_PROTOCOL_CHOICES,
                                       default=SSH
                                       )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name

class DevicePassword(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    username=models.CharField(max_length=255)
    password = models.CharField(max_length=255,default="user")
    status = models.BooleanField()
    applytodevice=models.BooleanField(default=False)
    description = models.TextField(null=True)
    
    valid_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class UserActivity(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    execute_time = models.DateTimeField()
    client_ip = models.GenericIPAddressField()
    command = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)




class WebUserActivity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=255)
    model_name = models.CharField(max_length=255)
    object_id = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)
    client_ip = models.GenericIPAddressField()
    description = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.user} - {self.action} - {self.model_name} - {self.object_id}"
