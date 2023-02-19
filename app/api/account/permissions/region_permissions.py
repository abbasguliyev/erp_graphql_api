from django_graphene_permissions.permissions import BasePermission

class RegionCreatePermissions(BasePermission):
    @staticmethod
    def has_permission(context):
        user = context.user
        permission_groups = user.groups.all()
        for permission_group in permission_groups:
            all_permissions = permission_group.permissions.all()
            for perm in all_permissions:
                if "add_region" == perm.codename or user.is_superuser:
                    return True

        if user.has_perm("add_region") or user.is_superuser:
            return True

class RegionUpdatePermissions(BasePermission):
    @staticmethod
    def has_permission(context):
        user = context.user
        permission_groups = user.groups.all()
        for permission_group in permission_groups:
            all_permissions = permission_group.permissions.all()
            for perm in all_permissions:
                if "change_region" == perm.codename or user.is_superuser:
                    return True

        if user.has_perm("change_region") or user.is_superuser:
            return True
       
class RegionDeletePermissions(BasePermission):
    @staticmethod
    def has_permission(context):
        user = context.user
        permission_groups = user.groups.all()
        for permission_group in permission_groups:
            all_permissions = permission_group.permissions.all()
            for perm in all_permissions:
                if "delete_region" == perm.codename or user.is_superuser:
                    return True

        if user.has_perm("delete_region") or user.is_superuser:
            return True

class RegionReadPermissions(BasePermission):
    @staticmethod
    def has_permission(context):
        user = context.user
        permission_groups = user.groups.all()
        for permission_group in permission_groups:
            all_permissions = permission_group.permissions.all()
            for perm in all_permissions:
                if "view_region" == perm.codename or user.is_superuser:
                    return True

        if user.has_perm("view_region") or user.is_superuser:
            return True     
