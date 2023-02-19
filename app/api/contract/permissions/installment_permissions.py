from django_graphene_permissions.permissions import BasePermission

class InstallmentCreatePermissions(BasePermission):
    @staticmethod
    def has_permission(context):
        user = context.user
        permission_groups = user.groups.all()
        for permission_group in permission_groups:
            all_permissions = permission_group.permissions.all()
            for perm in all_permissions:
                if "add_installment" == perm.codename or user.is_superuser:
                    return True

        if user.has_perm("add_installment") or user.is_superuser:
            return True

class InstallmentUpdatePermissions(BasePermission):
    @staticmethod
    def has_permission(context):
        user = context.user
        permission_groups = user.groups.all()
        for permission_group in permission_groups:
            all_permissions = permission_group.permissions.all()
            for perm in all_permissions:
                if "change_installment" == perm.codename or user.is_superuser:
                    return True

        if user.has_perm("change_installment") or user.is_superuser:
            return True
       
class InstallmentDeletePermissions(BasePermission):
    @staticmethod
    def has_permission(context):
        user = context.user
        permission_groups = user.groups.all()
        for permission_group in permission_groups:
            all_permissions = permission_group.permissions.all()
            for perm in all_permissions:
                if "delete_installment" == perm.codename or user.is_superuser:
                    return True

        if user.has_perm("delete_installment") or user.is_superuser:
            return True

class InstallmentReadPermissions(BasePermission):
    @staticmethod
    def has_permission(context):
        user = context.user
        permission_groups = user.groups.all()
        for permission_group in permission_groups:
            all_permissions = permission_group.permissions.all()
            for perm in all_permissions:
                if "view_installment" == perm.codename or user.is_superuser:
                    return True

        if user.has_perm("view_installment") or user.is_superuser:
            return True     
