from django.contrib import admin
from .models import  deviceGroup,  Device, DevicePassword, UserActivity,WebUserActivity

@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ['name', 'ip', 'group', 'status', 'access_protocol']
    search_fields = ['name', 'ip']  # Allows searching by name and IP address
    list_filter = ['group', 'access_protocol', 'status']  # Adds filter options in the sidebar

    def get_ordering(self, request):
        return ['group', 'name']


admin.site.register(deviceGroup)

admin.site.register(DevicePassword)
admin.site.register(UserActivity)
admin.site.register(WebUserActivity)
