from rest_framework.permissions import IsAdminUser, BasePermission


class IsStaffUser(IsAdminUser):
    """
    Allows access to Staff and Managers only.
    """
    pass


class IsManagerUser(BasePermission):
    """
    Allows access to Managers only.
    """

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_staff
        )
