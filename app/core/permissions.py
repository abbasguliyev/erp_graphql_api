from django_graphene_permissions.permissions import BasePermission

class IsAdminUser(BasePermission):
    @staticmethod
    def has_permission(context):
        return bool(context.user and context.user.is_staff)
