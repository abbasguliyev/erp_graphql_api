from django_graphene_permissions.permissions import BasePermission

class CompanyCreatePermissions(BasePermission):
    @staticmethod
    def has_permission(context):
        user = context.user
        permission_groups = user.groups.all()
        for permission_group in permission_groups:
            all_permissions = permission_group.permissions.all()
            for perm in all_permissions:
                if "add_company" == perm.codename or user.is_superuser:
                    return True

        if user.has_perm("add_company") or user.is_superuser:
            return True

class CompanyUpdatePermissions(BasePermission):
    @staticmethod
    def has_permission(context):
        user = context.user
        permission_groups = user.groups.all()
        for permission_group in permission_groups:
            all_permissions = permission_group.permissions.all()
            for perm in all_permissions:
                if "change_company" == perm.codename or user.is_superuser:
                    return True

        if user.has_perm("change_company") or user.is_superuser:
            return True
       
class CompanyDeletePermissions(BasePermission):
    @staticmethod
    def has_permission(context):
        user = context.user
        permission_groups = user.groups.all()
        for permission_group in permission_groups:
            all_permissions = permission_group.permissions.all()
            for perm in all_permissions:
                if "delete_company" == perm.codename or user.is_superuser:
                    return True

        if user.has_perm("delete_company") or user.is_superuser:
            return True

class CompanyReadPermissions(BasePermission):
    @staticmethod
    def has_permission(context):
        user = context.user
        permission_groups = user.groups.all()
        for permission_group in permission_groups:
            all_permissions = permission_group.permissions.all()
            for perm in all_permissions:
                if "view_company" == perm.codename or user.is_superuser:
                    return True

        if user.has_perm("view_company") or user.is_superuser:
            return True     
