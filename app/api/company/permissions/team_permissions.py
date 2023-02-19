from django_graphene_permissions.permissions import BasePermission

class TeamCreatePermissions(BasePermission):
    @staticmethod
    def has_permission(context):
        user = context.user
        permission_groups = user.groups.all()
        for permission_group in permission_groups:
            all_permissions = permission_group.permissions.all()
            for perm in all_permissions:
                if "add_team" == perm.codename or user.is_superuser:
                    return True

        if user.has_perm("add_team") or user.is_superuser:
            return True

class TeamUpdatePermissions(BasePermission):
    @staticmethod
    def has_permission(context):
        user = context.user
        permission_groups = user.groups.all()
        for permission_group in permission_groups:
            all_permissions = permission_group.permissions.all()
            for perm in all_permissions:
                if "change_team" == perm.codename or user.is_superuser:
                    return True

        if user.has_perm("change_team") or user.is_superuser:
            return True
       
class TeamDeletePermissions(BasePermission):
    @staticmethod
    def has_permission(context):
        user = context.user
        permission_groups = user.groups.all()
        for permission_group in permission_groups:
            all_permissions = permission_group.permissions.all()
            for perm in all_permissions:
                if "delete_team" == perm.codename or user.is_superuser:
                    return True

        if user.has_perm("delete_team") or user.is_superuser:
            return True

class TeamReadPermissions(BasePermission):
    @staticmethod
    def has_permission(context):
        user = context.user
        permission_groups = user.groups.all()
        for permission_group in permission_groups:
            all_permissions = permission_group.permissions.all()
            for perm in all_permissions:
                if "view_team" == perm.codename or user.is_superuser:
                    return True

        if user.has_perm("view_team") or user.is_superuser:
            return True     
