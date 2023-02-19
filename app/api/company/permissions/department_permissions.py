from django_graphene_permissions.permissions import BasePermission

class DepartmentCreatePermissions(BasePermission):
    @staticmethod
    def has_permission(context):
        user = context.user
        permission_groups = user.groups.all()
        for permission_group in permission_groups:
            all_permissions = permission_group.permissions.all()
            for perm in all_permissions:
                if "add_department" == perm.codename or user.is_superuser:
                    return True

        if user.has_perm("add_department") or user.is_superuser:
            return True

class DepartmentUpdatePermissions(BasePermission):
    @staticmethod
    def has_permission(context):
        user = context.user
        permission_groups = user.groups.all()
        for permission_group in permission_groups:
            all_permissions = permission_group.permissions.all()
            for perm in all_permissions:
                if "change_department" == perm.codename or user.is_superuser:
                    return True

        if user.has_perm("change_department") or user.is_superuser:
            return True
       
class DepartmentDeletePermissions(BasePermission):
    @staticmethod
    def has_permission(context):
        user = context.user
        permission_groups = user.groups.all()
        for permission_group in permission_groups:
            all_permissions = permission_group.permissions.all()
            for perm in all_permissions:
                if "delete_department" == perm.codename or user.is_superuser:
                    return True

        if user.has_perm("delete_department") or user.is_superuser:
            return True

class DepartmentReadPermissions(BasePermission):
    @staticmethod
    def has_permission(context):
        user = context.user
        permission_groups = user.groups.all()
        for permission_group in permission_groups:
            all_permissions = permission_group.permissions.all()
            for perm in all_permissions:
                if "view_department" == perm.codename or user.is_superuser:
                    return True

        if user.has_perm("view_department") or user.is_superuser:
            return True     
