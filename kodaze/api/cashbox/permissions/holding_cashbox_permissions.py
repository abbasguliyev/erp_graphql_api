from django_graphene_permissions.permissions import BasePermission

class HoldingCashboxCreatePermissions(BasePermission):
    @staticmethod
    def has_permission(context):
        user = context.user
        permission_groups = user.groups.all()
        for permission_group in permission_groups:
            all_permissions = permission_group.permissions.all()
            for perm in all_permissions:
                if "add_holdingcashbox" == perm.codename or user.is_superuser:
                    return True

        if user.has_perm("add_holdingcashbox") or user.is_superuser:
            return True

class HoldingCashboxUpdatePermissions(BasePermission):
    @staticmethod
    def has_permission(context):
        user = context.user
        permission_groups = user.groups.all()
        for permission_group in permission_groups:
            all_permissions = permission_group.permissions.all()
            for perm in all_permissions:
                if "change_holdingcashbox" == perm.codename or user.is_superuser:
                    return True

        if user.has_perm("change_holdingcashbox") or user.is_superuser:
            return True
       
class HoldingCashboxDeletePermissions(BasePermission):
    @staticmethod
    def has_permission(context):
        user = context.user
        permission_groups = user.groups.all()
        for permission_group in permission_groups:
            all_permissions = permission_group.permissions.all()
            for perm in all_permissions:
                if "delete_holdingcashbox" == perm.codename or user.is_superuser:
                    return True

        if user.has_perm("delete_holdingcashbox") or user.is_superuser:
            return True

class HoldingCashboxReadPermissions(BasePermission):
    @staticmethod
    def has_permission(context):
        user = context.user
        permission_groups = user.groups.all()
        for permission_group in permission_groups:
            all_permissions = permission_group.permissions.all()
            for perm in all_permissions:
                if "view_holdingcashbox" == perm.codename or user.is_superuser:
                    return True

        if user.has_perm("view_holdingcashbox") or user.is_superuser:
            return True     
