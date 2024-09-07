from django.contrib.auth import get_user_model
from rest_framework import serializers
from djoser.serializers import (
    UserCreatePasswordRetypeSerializer,
    UserSerializer)
from rest_framework.exceptions import ValidationError
from validation import (validate_password, validate_email)

User = get_user_model()


class UserRegistrationSerializer(UserCreatePasswordRetypeSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(required=True)
    name = serializers.CharField(required=True)
    surname = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password",
            "name",
            "surname",
        ]

    def validate(self, attrs):
        email = attrs.get("email")
        self.fields.pop("re_password", None)
        password = attrs.get("password")
        password2 = attrs.pop("re_password")
        if password != password2:
            raise ValidationError({"password": "Passwords are different"})
        try:
            validate_email.validate_email(email)
        except ValidationError as e:
            raise ValidationError({"email": e.detail})
        try:
            validate_password.validate_password(password)
        except ValidationError as e:
            raise ValidationError({"password": e.detail})
        return attrs


class UserListSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        model = User
        fields = [
            "uuid",
            "username",
            "email",
            "name",
            "surname",
            "is_staff",
        ]


class UserSerializer(serializers.Serializer):
    uuid = serializers.UUIDField()
    username = serializers.CharField()