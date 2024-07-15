from string import punctuation

import zxcvbn
from rest_framework.exceptions import ValidationError


def validate_password(password_to_validate, email=None, first_name=None, surname=None):
    if len(password_to_validate) < 8:
        raise ValidationError("Password length should be at least 8 characters ")
    if (not any(symbol.isdigit() for symbol in password_to_validate)
            or not any(symbol.islower() for symbol in password_to_validate)
            or not any(symbol.isupper() for symbol in password_to_validate)
            or not any(symbol in punctuation for symbol in password_to_validate)):
        raise ValidationError(
            "Password should include at least one uppercase latter, one lowercase letter, one digit and one symbol")
    complexity = zxcvbn.zxcvbn(password_to_validate, user_inputs=[email, first_name, surname])
    if complexity["score"] <= 2:
        raise ValidationError("Password is weak, please enter another one")

    return password_to_validate
