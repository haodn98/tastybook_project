from rest_framework.permissions import BasePermission


class IsImageOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.created_by == request.user
