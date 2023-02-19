from django_graphene_permissions.permissions import BasePermission

class CustomerCreatePermissions(BasePermission):
    @staticmethod
    def has_permission(context):
        user = context.user
        permission_groups = user.groups.all()
        for permission_group in permission_groups:
            all_permissions = permission_group.permissions.all()
            for perm in all_permissions:
                if "add_customer" == perm.codename or user.is_superuser:
                    return True

        if user.has_perm("add_customer") or user.is_superuser:
            return True

class CustomerUpdatePermissions(BasePermission):
    @staticmethod
    def has_permission(context):
        user = context.user
        permission_groups = user.groups.all()
        for permission_group in permission_groups:
            all_permissions = permission_group.permissions.all()
            for perm in all_permissions:
                if "change_customer" == perm.codename or user.is_superuser:
                    return True

        if user.has_perm("change_customer") or user.is_superuser:
            return True
       
class CustomerDeletePermissions(BasePermission):
    @staticmethod
    def has_permission(context):
        user = context.user
        permission_groups = user.groups.all()
        for permission_group in permission_groups:
            all_permissions = permission_group.permissions.all()
            for perm in all_permissions:
                if "delete_customer" == perm.codename or user.is_superuser:
                    return True

        if user.has_perm("delete_customer") or user.is_superuser:
            return True

class CustomerReadPermissions(BasePermission):
    @staticmethod
    def has_permission(context):
        user = context.user
        permission_groups = user.groups.all()
        for permission_group in permission_groups:
            all_permissions = permission_group.permissions.all()
            for perm in all_permissions:
                if "view_customer" == perm.codename or user.is_superuser:
                    return True

        if user.has_perm("view_customer") or user.is_superuser:
            return True     
