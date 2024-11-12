from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from .models import DevicePassword, Device  # Import Device model
from .ssh_utils import ssh_apply_device_password

@receiver(post_save, sender=DevicePassword)
def apply_device_password(sender, instance, created, **kwargs):
    if created and instance.status and instance.valid_time > timezone.now() and not instance.applytodevice:
        device = instance.device
        if device.access_protocol == Device.SSH:
            ssh_apply_device_password(device.ip, device.port, device.remote_user, device.remote_password, instance.username, instance.password,instance.valid_time)
            instance.applytodevice = True
            instance.save()
