from django_graphene_permissions.permissions import BasePermission

class ContractCreatePermissions(BasePermission):
    @staticmethod
    def has_permission(context):
        user = context.user
        permission_groups = user.groups.all()
        for permission_group in permission_groups:
            all_permissions = permission_group.permissions.all()
            for perm in all_permissions:
                if "add_contract" == perm.codename or user.is_superuser:
                    return True

        if user.has_perm("add_contract") or user.is_superuser:
            return True

class ContractUpdatePermissions(BasePermission):
    @staticmethod
    def has_permission(context):
        user = context.user
        permission_groups = user.groups.all()
        for permission_group in permission_groups:
            all_permissions = permission_group.permissions.all()
            for perm in all_permissions:
                if "change_contract" == perm.codename or user.is_superuser:
                    return True

        if user.has_perm("change_contract") or user.is_superuser:
            return True
       
class ContractDeletePermissions(BasePermission):
    @staticmethod
    def has_permission(context):
        user = context.user
        permission_groups = user.groups.all()
        for permission_group in permission_groups:
            all_permissions = permission_group.permissions.all()
            for perm in all_permissions:
                if "delete_contract" == perm.codename or user.is_superuser:
                    return True

        if user.has_perm("delete_contract") or user.is_superuser:
            return True

class ContractReadPermissions(BasePermission):
    @staticmethod
    def has_permission(context):
        user = context.user
        permission_groups = user.groups.all()
        for permission_group in permission_groups:
            all_permissions = permission_group.permissions.all()
            for perm in all_permissions:
                if "view_contract" == perm.codename or user.is_superuser:
                    return True

        if user.has_perm("view_contract") or user.is_superuser:
            return True     
