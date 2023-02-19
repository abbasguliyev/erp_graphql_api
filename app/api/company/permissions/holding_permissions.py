from django_graphene_permissions.permissions import BasePermission

class HoldingCreatePermissions(BasePermission):
    @staticmethod
    def has_permission(context):
        user = context.user
        permission_groups = user.groups.all()
        for permission_group in permission_groups:
            all_permissions = permission_group.permissions.all()
            for perm in all_permissions:
                if "add_holding" == perm.codename or user.is_superuser:
                    return True

        if user.has_perm("add_holding") or user.is_superuser:
            return True

class HoldingUpdatePermissions(BasePermission):
    @staticmethod
    def has_permission(context):
        user = context.user
        permission_groups = user.groups.all()
        for permission_group in permission_groups:
            all_permissions = permission_group.permissions.all()
            for perm in all_permissions:
                if "change_holding" == perm.codename or user.is_superuser:
                    return True

        if user.has_perm("change_holding") or user.is_superuser:
            return True
       
class HoldingDeletePermissions(BasePermission):
    @staticmethod
    def has_permission(context):
        user = context.user
        permission_groups = user.groups.all()
        for permission_group in permission_groups:
            all_permissions = permission_group.permissions.all()
            for perm in all_permissions:
                if "delete_holding" == perm.codename or user.is_superuser:
                    return True

        if user.has_perm("delete_holding") or user.is_superuser:
            return True

class HoldingReadPermissions(BasePermission):
    @staticmethod
    def has_permission(context):
        user = context.user
        permission_groups = user.groups.all()
        for permission_group in permission_groups:
            all_permissions = permission_group.permissions.all()
            for perm in all_permissions:
                if "view_holding" == perm.codename or user.is_superuser:
                    return True

        if user.has_perm("view_holding") or user.is_superuser:
            return True     
