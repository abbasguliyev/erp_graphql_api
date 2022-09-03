from django_graphene_permissions.permissions import BasePermission

class PermissionForPositionCreatePermissions(BasePermission):
    @staticmethod
    def has_permission(context):
        user = context.user
        permission_groups = user.groups.all()
        for permission_group in permission_groups:
            all_permissions = permission_group.permissions.all()
            for perm in all_permissions:
                if "add_permissionforposition" == perm.codename or user.is_superuser:
                    return True

        if user.has_perm("add_permissionforposition") or user.is_superuser:
            return True

class PermissionForPositionUpdatePermissions(BasePermission):
    @staticmethod
    def has_permission(context):
        user = context.user
        permission_groups = user.groups.all()
        for permission_group in permission_groups:
            all_permissions = permission_group.permissions.all()
            for perm in all_permissions:
                if "change_permissionforposition" == perm.codename or user.is_superuser:
                    return True

        if user.has_perm("change_permissionforposition") or user.is_superuser:
            return True
       
class PermissionForPositionDeletePermissions(BasePermission):
    @staticmethod
    def has_permission(context):
        user = context.user
        permission_groups = user.groups.all()
        for permission_group in permission_groups:
            all_permissions = permission_group.permissions.all()
            for perm in all_permissions:
                if "delete_permissionforposition" == perm.codename or user.is_superuser:
                    return True

        if user.has_perm("delete_permissionforposition") or user.is_superuser:
            return True

class PermissionForPositionReadPermissions(BasePermission):
    @staticmethod
    def has_permission(context):
        user = context.user
        permission_groups = user.groups.all()
        for permission_group in permission_groups:
            all_permissions = permission_group.permissions.all()
            for perm in all_permissions:
                if "view_permissionforposition" == perm.codename or user.is_superuser:
                    return True

        if user.has_perm("view_permissionforposition") or user.is_superuser:
            return True     
