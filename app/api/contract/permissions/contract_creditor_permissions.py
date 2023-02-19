from django_graphene_permissions.permissions import BasePermission

class ContractCreditorCreatePermissions(BasePermission):
    @staticmethod
    def has_permission(context):
        user = context.user
        permission_groups = user.groups.all()
        for permission_group in permission_groups:
            all_permissions = permission_group.permissions.all()
            for perm in all_permissions:
                if "add_contractcreditor" == perm.codename or user.is_superuser:
                    return True

        if user.has_perm("add_contractcreditor") or user.is_superuser:
            return True

class ContractCreditorUpdatePermissions(BasePermission):
    @staticmethod
    def has_permission(context):
        user = context.user
        permission_groups = user.groups.all()
        for permission_group in permission_groups:
            all_permissions = permission_group.permissions.all()
            for perm in all_permissions:
                if "change_contractcreditor" == perm.codename or user.is_superuser:
                    return True

        if user.has_perm("change_contractcreditor") or user.is_superuser:
            return True
       
class ContractCreditorDeletePermissions(BasePermission):
    @staticmethod
    def has_permission(context):
        user = context.user
        permission_groups = user.groups.all()
        for permission_group in permission_groups:
            all_permissions = permission_group.permissions.all()
            for perm in all_permissions:
                if "delete_contractcreditor" == perm.codename or user.is_superuser:
                    return True

        if user.has_perm("delete_contractcreditor") or user.is_superuser:
            return True

class ContractCreditorReadPermissions(BasePermission):
    @staticmethod
    def has_permission(context):
        user = context.user
        permission_groups = user.groups.all()
        for permission_group in permission_groups:
            all_permissions = permission_group.permissions.all()
            for perm in all_permissions:
                if "view_contractcreditor" == perm.codename or user.is_superuser:
                    return True

        if user.has_perm("view_contractcreditor") or user.is_superuser:
            return True     
