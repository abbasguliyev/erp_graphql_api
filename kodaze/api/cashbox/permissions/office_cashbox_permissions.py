from django_graphene_permissions.permissions import BasePermission

class OfficeCashboxCreatePermissions(BasePermission):
    @staticmethod
    def has_permission(context):
        user = context.user
        permission_groups = user.groups.all()
        for permission_group in permission_groups:
            all_permissions = permission_group.permissions.all()
            for perm in all_permissions:
                if "add_officecashbox" == perm.codename or user.is_superuser:
                    return True

        if user.has_perm("add_officecashbox") or user.is_superuser:
            return True

class OfficeCashboxUpdatePermissions(BasePermission):
    @staticmethod
    def has_permission(context):
        user = context.user
        permission_groups = user.groups.all()
        for permission_group in permission_groups:
            all_permissions = permission_group.permissions.all()
            for perm in all_permissions:
                if "change_officecashbox" == perm.codename or user.is_superuser:
                    return True

        if user.has_perm("change_officecashbox") or user.is_superuser:
            return True
       
class OfficeCashboxDeletePermissions(BasePermission):
    @staticmethod
    def has_permission(context):
        user = context.user
        permission_groups = user.groups.all()
        for permission_group in permission_groups:
            all_permissions = permission_group.permissions.all()
            for perm in all_permissions:
                if "delete_officecashbox" == perm.codename or user.is_superuser:
                    return True

        if user.has_perm("delete_officecashbox") or user.is_superuser:
            return True

class OfficeCashboxReadPermissions(BasePermission):
    @staticmethod
    def has_permission(context):
        user = context.user
        permission_groups = user.groups.all()
        for permission_group in permission_groups:
            all_permissions = permission_group.permissions.all()
            for perm in all_permissions:
                if "view_officecashbox" == perm.codename or user.is_superuser:
                    return True

        if user.has_perm("view_officecashbox") or user.is_superuser:
            return True     
