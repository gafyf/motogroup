from django.core.exceptions import ValidationError
import re

def validate_password(value):
    if not re.search(r'[A-Z]', value):
        raise ValidationError("The password must contain at least one capital letter.")
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', value):
        raise ValidationError("The password must contain at least one special character.")
