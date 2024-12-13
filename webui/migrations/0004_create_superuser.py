from django.db import migrations

from django.db import migrations

def create_superuser(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    
    # Check if the admin user already exists
    admin_user = User.objects.filter(username='admin').first()
    
    # If the admin user exists, delete them
    if admin_user:
        admin_user.delete()
    
    # Create a new admin user
    User.objects.create_superuser(
        username='admin',
        email='admin@example.com',
        password='iman'
    )



class Migration(migrations.Migration):

    dependencies = [
        ('webui', '0003_device_port'),  # Update this to match the correct previous migration
    ]

    operations = [
        migrations.RunPython(create_superuser),
    ]
