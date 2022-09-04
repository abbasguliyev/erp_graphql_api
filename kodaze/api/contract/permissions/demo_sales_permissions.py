from django_graphene_permissions.permissions import BasePermission

class DemoSalesCreatePermissions(BasePermission):
    @staticmethod
    def has_permission(context):
        user = context.user
        permission_groups = user.groups.all()
        for permission_group in permission_groups:
            all_permissions = permission_group.permissions.all()
            for perm in all_permissions:
                if "add_demosales" == perm.codename or user.is_superuser:
                    return True

        if user.has_perm("add_demosales") or user.is_superuser:
            return True

class DemoSalesUpdatePermissions(BasePermission):
    @staticmethod
    def has_permission(context):
        user = context.user
        permission_groups = user.groups.all()
        for permission_group in permission_groups:
            all_permissions = permission_group.permissions.all()
            for perm in all_permissions:
                if "change_demosales" == perm.codename or user.is_superuser:
                    return True

        if user.has_perm("change_demosales") or user.is_superuser:
            return True
       
class DemoSalesDeletePermissions(BasePermission):
    @staticmethod
    def has_permission(context):
        user = context.user
        permission_groups = user.groups.all()
        for permission_group in permission_groups:
            all_permissions = permission_group.permissions.all()
            for perm in all_permissions:
                if "delete_demosales" == perm.codename or user.is_superuser:
                    return True

        if user.has_perm("delete_demosales") or user.is_superuser:
            return True

class DemoSalesReadPermissions(BasePermission):
    @staticmethod
    def has_permission(context):
        user = context.user
        permission_groups = user.groups.all()
        for permission_group in permission_groups:
            all_permissions = permission_group.permissions.all()
            for perm in all_permissions:
                if "view_demosales" == perm.codename or user.is_superuser:
                    return True

        if user.has_perm("view_demosales") or user.is_superuser:
            return True     
