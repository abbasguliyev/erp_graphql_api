from django_graphene_permissions.permissions import BasePermission

class EmployeeStatusCreatePermissions(BasePermission):
    @staticmethod
    def has_permission(context):
        user = context.user
        permission_groups = user.groups.all()
        for permission_group in permission_groups:
            all_permissions = permission_group.permissions.all()
            for perm in all_permissions:
                if "add_employeestatus" == perm.codename or user.is_superuser:
                    return True

        if user.has_perm("add_employeestatus") or user.is_superuser:
            return True

class EmployeeStatusUpdatePermissions(BasePermission):
    @staticmethod
    def has_permission(context):
        user = context.user
        permission_groups = user.groups.all()
        for permission_group in permission_groups:
            all_permissions = permission_group.permissions.all()
            for perm in all_permissions:
                if "change_employeestatus" == perm.codename or user.is_superuser:
                    return True

        if user.has_perm("change_employeestatus") or user.is_superuser:
            return True
       
class EmployeeStatusDeletePermissions(BasePermission):
    @staticmethod
    def has_permission(context):
        user = context.user
        permission_groups = user.groups.all()
        for permission_group in permission_groups:
            all_permissions = permission_group.permissions.all()
            for perm in all_permissions:
                if "delete_employeestatus" == perm.codename or user.is_superuser:
                    return True

        if user.has_perm("delete_employeestatus") or user.is_superuser:
            return True

class EmployeeStatusReadPermissions(BasePermission):
    @staticmethod
    def has_permission(context):
        user = context.user
        permission_groups = user.groups.all()
        for permission_group in permission_groups:
            all_permissions = permission_group.permissions.all()
            for perm in all_permissions:
                if "view_employeestatus" == perm.codename or user.is_superuser:
                    return True

        if user.has_perm("view_employeestatus") or user.is_superuser:
            return True     
