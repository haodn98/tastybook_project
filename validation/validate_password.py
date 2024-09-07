from string import punctuation

from rest_framework.exceptions import ValidationError


def validate_password(password_to_validate):
    if len(password_to_validate) < 8:
        raise ValidationError("Password length should be at least 8 characters ")
    if (not any(symbol.isdigit() for symbol in password_to_validate)
            or not any(symbol.islower() for symbol in password_to_validate)
            or not any(symbol.isupper() for symbol in password_to_validate)
            or not any(symbol in punctuation for symbol in password_to_validate)):
        raise ValidationError(
            "Password should include at least one uppercase latter, one lowercase letter, one digit and one symbol")
    return password_to_validate