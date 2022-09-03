from django_graphene_permissions.permissions import BasePermission

class PositionCreatePermissions(BasePermission):
    @staticmethod
    def has_permission(context):
        user = context.user
        permission_groups = user.groups.all()
        for permission_group in permission_groups:
            all_permissions = permission_group.permissions.all()
            for perm in all_permissions:
                if "add_position" == perm.codename or user.is_superuser:
                    return True

        if user.has_perm("add_position") or user.is_superuser:
            return True

class PositionUpdatePermissions(BasePermission):
    @staticmethod
    def has_permission(context):
        user = context.user
        permission_groups = user.groups.all()
        for permission_group in permission_groups:
            all_permissions = permission_group.permissions.all()
            for perm in all_permissions:
                if "change_position" == perm.codename or user.is_superuser:
                    return True

        if user.has_perm("change_position") or user.is_superuser:
            return True
       
class PositionDeletePermissions(BasePermission):
    @staticmethod
    def has_permission(context):
        user = context.user
        permission_groups = user.groups.all()
        for permission_group in permission_groups:
            all_permissions = permission_group.permissions.all()
            for perm in all_permissions:
                if "delete_position" == perm.codename or user.is_superuser:
                    return True

        if user.has_perm("delete_position") or user.is_superuser:
            return True

class PositionReadPermissions(BasePermission):
    @staticmethod
    def has_permission(context):
        user = context.user
        permission_groups = user.groups.all()
        for permission_group in permission_groups:
            all_permissions = permission_group.permissions.all()
            for perm in all_permissions:
                if "view_position" == perm.codename or user.is_superuser:
                    return True

        if user.has_perm("view_position") or user.is_superuser:
            return True     
