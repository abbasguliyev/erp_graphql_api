from django_graphene_permissions.permissions import BasePermission

class CashFlowCreatePermissions(BasePermission):
    @staticmethod
    def has_permission(context):
        user = context.user
        permission_groups = user.groups.all()
        for permission_group in permission_groups:
            all_permissions = permission_group.permissions.all()
            for perm in all_permissions:
                if "add_cashflow" == perm.codename or user.is_superuser:
                    return True

        if user.has_perm("add_cashflow") or user.is_superuser:
            return True

class CashFlowUpdatePermissions(BasePermission):
    @staticmethod
    def has_permission(context):
        user = context.user
        permission_groups = user.groups.all()
        for permission_group in permission_groups:
            all_permissions = permission_group.permissions.all()
            for perm in all_permissions:
                if "change_cashflow" == perm.codename or user.is_superuser:
                    return True

        if user.has_perm("change_cashflow") or user.is_superuser:
            return True
       
class CashFlowDeletePermissions(BasePermission):
    @staticmethod
    def has_permission(context):
        user = context.user
        permission_groups = user.groups.all()
        for permission_group in permission_groups:
            all_permissions = permission_group.permissions.all()
            for perm in all_permissions:
                if "delete_cashflow" == perm.codename or user.is_superuser:
                    return True

        if user.has_perm("delete_cashflow") or user.is_superuser:
            return True

class CashFlowReadPermissions(BasePermission):
    @staticmethod
    def has_permission(context):
        user = context.user
        permission_groups = user.groups.all()
        for permission_group in permission_groups:
            all_permissions = permission_group.permissions.all()
            for perm in all_permissions:
                if "view_cashflow" == perm.codename or user.is_superuser:
                    return True

        if user.has_perm("view_cashflow") or user.is_superuser:
            return True     
