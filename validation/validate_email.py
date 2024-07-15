import re
from rest_framework.exceptions import ValidationError

def validate_email(email_to_validate: str):
    pattern = r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+'
    if not re.match(pattern, email_to_validate):
        raise ValidationError("Email is invalid")
    return email_to_validate
