from django_graphene_permissions.permissions import BasePermission

class ContractChangeCreatePermissions(BasePermission):
    @staticmethod
    def has_permission(context):
        user = context.user
        permission_groups = user.groups.all()
        for permission_group in permission_groups:
            all_permissions = permission_group.permissions.all()
            for perm in all_permissions:
                if "add_contractchange" == perm.codename or user.is_superuser:
                    return True

        if user.has_perm("add_contractchange") or user.is_superuser:
            return True

class ContractChangeUpdatePermissions(BasePermission):
    @staticmethod
    def has_permission(context):
        user = context.user
        permission_groups = user.groups.all()
        for permission_group in permission_groups:
            all_permissions = permission_group.permissions.all()
            for perm in all_permissions:
                if "change_contractchange" == perm.codename or user.is_superuser:
                    return True

        if user.has_perm("change_contractchange") or user.is_superuser:
            return True
       
class ContractChangeDeletePermissions(BasePermission):
    @staticmethod
    def has_permission(context):
        user = context.user
        permission_groups = user.groups.all()
        for permission_group in permission_groups:
            all_permissions = permission_group.permissions.all()
            for perm in all_permissions:
                if "delete_contractchange" == perm.codename or user.is_superuser:
                    return True

        if user.has_perm("delete_contractchange") or user.is_superuser:
            return True

class ContractChangeReadPermissions(BasePermission):
    @staticmethod
    def has_permission(context):
        user = context.user
        permission_groups = user.groups.all()
        for permission_group in permission_groups:
            all_permissions = permission_group.permissions.all()
            for perm in all_permissions:
                if "view_contractchange" == perm.codename or user.is_superuser:
                    return True

        if user.has_perm("view_contractchange") or user.is_superuser:
            return True     
