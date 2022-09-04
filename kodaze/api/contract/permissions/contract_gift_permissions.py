from django_graphene_permissions.permissions import BasePermission

class ContractGiftCreatePermissions(BasePermission):
    @staticmethod
    def has_permission(context):
        user = context.user
        permission_groups = user.groups.all()
        for permission_group in permission_groups:
            all_permissions = permission_group.permissions.all()
            for perm in all_permissions:
                if "add_contractgift" == perm.codename or user.is_superuser:
                    return True

        if user.has_perm("add_contractgift") or user.is_superuser:
            return True

class ContractGiftUpdatePermissions(BasePermission):
    @staticmethod
    def has_permission(context):
        user = context.user
        permission_groups = user.groups.all()
        for permission_group in permission_groups:
            all_permissions = permission_group.permissions.all()
            for perm in all_permissions:
                if "change_contractgift" == perm.codename or user.is_superuser:
                    return True

        if user.has_perm("change_contractgift") or user.is_superuser:
            return True
       
class ContractGiftDeletePermissions(BasePermission):
    @staticmethod
    def has_permission(context):
        user = context.user
        permission_groups = user.groups.all()
        for permission_group in permission_groups:
            all_permissions = permission_group.permissions.all()
            for perm in all_permissions:
                if "delete_contractgift" == perm.codename or user.is_superuser:
                    return True

        if user.has_perm("delete_contractgift") or user.is_superuser:
            return True

class ContractGiftReadPermissions(BasePermission):
    @staticmethod
    def has_permission(context):
        user = context.user
        permission_groups = user.groups.all()
        for permission_group in permission_groups:
            all_permissions = permission_group.permissions.all()
            for perm in all_permissions:
                if "view_contractgift" == perm.codename or user.is_superuser:
                    return True

        if user.has_perm("view_contractgift") or user.is_superuser:
            return True     
