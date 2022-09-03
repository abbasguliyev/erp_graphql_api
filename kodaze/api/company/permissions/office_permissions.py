from django_graphene_permissions.permissions import BasePermission

class OfficeCreatePermissions(BasePermission):
    @staticmethod
    def has_permission(context):
        user = context.user
        permission_groups = user.groups.all()
        for permission_group in permission_groups:
            all_permissions = permission_group.permissions.all()
            for perm in all_permissions:
                if "add_office" == perm.codename or user.is_superuser:
                    return True

        if user.has_perm("add_office") or user.is_superuser:
            return True

class OfficeUpdatePermissions(BasePermission):
    @staticmethod
    def has_permission(context):
        user = context.user
        permission_groups = user.groups.all()
        for permission_group in permission_groups:
            all_permissions = permission_group.permissions.all()
            for perm in all_permissions:
                if "change_office" == perm.codename or user.is_superuser:
                    return True

        if user.has_perm("change_office") or user.is_superuser:
            return True
       
class OfficeDeletePermissions(BasePermission):
    @staticmethod
    def has_permission(context):
        user = context.user
        permission_groups = user.groups.all()
        for permission_group in permission_groups:
            all_permissions = permission_group.permissions.all()
            for perm in all_permissions:
                if "delete_office" == perm.codename or user.is_superuser:
                    return True

        if user.has_perm("delete_office") or user.is_superuser:
            return True

class OfficeReadPermissions(BasePermission):
    @staticmethod
    def has_permission(context):
        user = context.user
        permission_groups = user.groups.all()
        for permission_group in permission_groups:
            all_permissions = permission_group.permissions.all()
            for perm in all_permissions:
                if "view_office" == perm.codename or user.is_superuser:
                    return True

        if user.has_perm("view_office") or user.is_superuser:
            return True     
