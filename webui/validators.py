from django.core.exceptions import ValidationError
import ipaddress

def validate_ip_address(value):
    try:
        ipaddress.ip_address(value)
    except ValueError:
        raise ValidationError(f'{value} is not a valid IP address')
