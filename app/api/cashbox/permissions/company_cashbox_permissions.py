from django_graphene_permissions.permissions import BasePermission

class CompanyCashboxCreatePermissions(BasePermission):
    @staticmethod
    def has_permission(context):
        user = context.user
        permission_groups = user.groups.all()
        for permission_group in permission_groups:
            all_permissions = permission_group.permissions.all()
            for perm in all_permissions:
                if "add_companycashbox" == perm.codename or user.is_superuser:
                    return True

        if user.has_perm("add_companycashbox") or user.is_superuser:
            return True

class CompanyCashboxUpdatePermissions(BasePermission):
    @staticmethod
    def has_permission(context):
        user = context.user
        permission_groups = user.groups.all()
        for permission_group in permission_groups:
            all_permissions = permission_group.permissions.all()
            for perm in all_permissions:
                if "change_companycashbox" == perm.codename or user.is_superuser:
                    return True

        if user.has_perm("change_companycashbox") or user.is_superuser:
            return True
       
class CompanyCashboxDeletePermissions(BasePermission):
    @staticmethod
    def has_permission(context):
        user = context.user
        permission_groups = user.groups.all()
        for permission_group in permission_groups:
            all_permissions = permission_group.permissions.all()
            for perm in all_permissions:
                if "delete_companycashbox" == perm.codename or user.is_superuser:
                    return True

        if user.has_perm("delete_companycashbox") or user.is_superuser:
            return True

class CompanyCashboxReadPermissions(BasePermission):
    @staticmethod
    def has_permission(context):
        user = context.user
        permission_groups = user.groups.all()
        for permission_group in permission_groups:
            all_permissions = permission_group.permissions.all()
            for perm in all_permissions:
                if "view_companycashbox" == perm.codename or user.is_superuser:
                    return True

        if user.has_perm("view_companycashbox") or user.is_superuser:
            return True     
