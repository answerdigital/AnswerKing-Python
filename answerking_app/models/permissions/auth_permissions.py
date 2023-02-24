from rest_framework.permissions import IsAdminUser, BasePermission


class IsStaffUser(IsAdminUser):
    """
    Allows access to Staff and Managers only.
    """

    pass


class IsManagerUser(BasePermission):
    """
    Allows access to Manager's only.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_staff)


class IsOwner(BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return bool(obj.owner == request.user)
