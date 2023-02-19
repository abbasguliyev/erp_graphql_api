from django_graphene_permissions.permissions import BasePermission

class UserCreatePermissions(BasePermission):
    @staticmethod
    def has_permission(context):
        user = context.user
        permission_groups = user.groups.all()
        for permission_group in permission_groups:
            all_permissions = permission_group.permissions.all()
            for perm in all_permissions:
                if "add_user" == perm.codename or user.is_superuser:
                    return True

        if user.has_perm("add_user") or user.is_superuser:
            return True

class UserUpdatePermissions(BasePermission):
    @staticmethod
    def has_permission(context):
        user = context.user
        permission_groups = user.groups.all()
        for permission_group in permission_groups:
            all_permissions = permission_group.permissions.all()
            for perm in all_permissions:
                if "change_user" == perm.codename or user.is_superuser:
                    return True

        if user.has_perm("change_user") or user.is_superuser:
            return True
       
class UserDeletePermissions(BasePermission):
    @staticmethod
    def has_permission(context):
        user = context.user
        permission_groups = user.groups.all()
        for permission_group in permission_groups:
            all_permissions = permission_group.permissions.all()
            for perm in all_permissions:
                if "delete_user" == perm.codename or user.is_superuser:
                    return True

        if user.has_perm("delete_user") or user.is_superuser:
            return True

class UserReadPermissions(BasePermission):
    @staticmethod
    def has_permission(context):
        user = context.user
        permission_groups = user.groups.all()
        for permission_group in permission_groups:
            all_permissions = permission_group.permissions.all()
            for perm in all_permissions:
                if "view_user" == perm.codename or user.is_superuser:
                    return True

        if user.has_perm("view_user") or user.is_superuser:
            return True     
