from django_graphene_permissions.permissions import BasePermission

class AppLogoCreatePermissions(BasePermission):
    @staticmethod
    def has_permission(context):
        user = context.user
        permission_groups = user.groups.all()
        for permission_group in permission_groups:
            all_permissions = permission_group.permissions.all()
            for perm in all_permissions:
                if "add_applogo" == perm.codename or user.is_superuser:
                    return True

        if user.has_perm("add_applogo") or user.is_superuser:
            return True

class AppLogoUpdatePermissions(BasePermission):
    @staticmethod
    def has_permission(context):
        user = context.user
        permission_groups = user.groups.all()
        for permission_group in permission_groups:
            all_permissions = permission_group.permissions.all()
            for perm in all_permissions:
                if "change_applogo" == perm.codename or user.is_superuser:
                    return True

        if user.has_perm("change_applogo") or user.is_superuser:
            return True
       
class AppLogoDeletePermissions(BasePermission):
    @staticmethod
    def has_permission(context):
        user = context.user
        permission_groups = user.groups.all()
        for permission_group in permission_groups:
            all_permissions = permission_group.permissions.all()
            for perm in all_permissions:
                if "delete_applogo" == perm.codename or user.is_superuser:
                    return True

        if user.has_perm("delete_applogo") or user.is_superuser:
            return True

class AppLogoReadPermissions(BasePermission):
    @staticmethod
    def has_permission(context):
        user = context.user
        permission_groups = user.groups.all()
        for permission_group in permission_groups:
            all_permissions = permission_group.permissions.all()
            for perm in all_permissions:
                if "view_applogo" == perm.codename or user.is_superuser:
                    return True

        if user.has_perm("view_applogo") or user.is_superuser:
            return True     
