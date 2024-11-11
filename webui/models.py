from django.db import models
from django.contrib.auth.models import AbstractUser,User,BaseUserManager



class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, email, password, **extra_fields)

    def delete_user(self, user_id):
        user = self.get(pk=user_id)
        user.delete()

    def disable_user(self, user_id):
        user = self.get(pk=user_id)
        user.is_active = False
        user.save()

    def modify_password(self, user_id, new_password):
        user = self.get(pk=user_id)
        user.set_password(new_password)
        user.save()

class userdData(AbstractUser):
    user = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='custom_users')
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    user_level = models.SmallIntegerField()
    status = models.BigIntegerField()
    admin = models.BooleanField()
    
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='userd_data_set',  # Add this related_name to avoid conflict
        blank=True,
        help_text=('The groups this user belongs to. A user will get all permissions granted to each of their groups.'),
        related_query_name='userd_data',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='userd_data_set',  # Add this related_name to avoid conflict
        blank=True,
        help_text=('Specific permissions for this user.'),
        related_query_name='userd_data',
    )

    objects = UserManager()



class deviceGroup(models.Model):
    name = models.CharField(max_length=255)
    icon = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    status = models.BooleanField() 
    def __str__(self):
        return self.name

class GroupAccess(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(deviceGroup, on_delete=models.CASCADE)
    view = models.BooleanField()
    create_user = models.BooleanField()
    status = models.BooleanField(default=True)

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
    domain_name = models.CharField(max_length=255, null=True, blank=True)
    status = models.BooleanField()
    remote_user = models.CharField(max_length=255)
    remote_password = models.CharField(max_length=255)
    access_protocol = models.CharField(max_length=10,
                                       choices=ACCESS_PROTOCOL_CHOICES,
                                       default=SSH
                                       )
    def __str__(self):
        return self.name

class DevicePassword(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    password = models.CharField(max_length=255)
    status = models.BooleanField()
    description = models.TextField(null=True)
    valid_time = models.DateTimeField()

class UserActivity(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    execute_time = models.DateTimeField()
    client_ip = models.GenericIPAddressField()
    command = models.TextField()
