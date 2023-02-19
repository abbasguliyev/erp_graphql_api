from django_graphene_permissions.permissions import BasePermission

class CategoryCreatePermissions(BasePermission):
    @staticmethod
    def has_permission(context):
        user = context.user
        permission_groups = user.groups.all()
        for permission_group in permission_groups:
            all_permissions = permission_group.permissions.all()
            for perm in all_permissions:
                if "add_category" == perm.codename or user.is_superuser:
                    return True

        if user.has_perm("add_category") or user.is_superuser:
            return True

class CategoryUpdatePermissions(BasePermission):
    @staticmethod
    def has_permission(context):
        user = context.user
        permission_groups = user.groups.all()
        for permission_group in permission_groups:
            all_permissions = permission_group.permissions.all()
            for perm in all_permissions:
                if "change_category" == perm.codename or user.is_superuser:
                    return True

        if user.has_perm("change_category") or user.is_superuser:
            return True
       
class CategoryDeletePermissions(BasePermission):
    @staticmethod
    def has_permission(context):
        user = context.user
        permission_groups = user.groups.all()
        for permission_group in permission_groups:
            all_permissions = permission_group.permissions.all()
            for perm in all_permissions:
                if "delete_category" == perm.codename or user.is_superuser:
                    return True

        if user.has_perm("delete_category") or user.is_superuser:
            return True

class CategoryReadPermissions(BasePermission):
    @staticmethod
    def has_permission(context):
        user = context.user
        permission_groups = user.groups.all()
        for permission_group in permission_groups:
            all_permissions = permission_group.permissions.all()
            for perm in all_permissions:
                if "view_category" == perm.codename or user.is_superuser:
                    return True

        if user.has_perm("view_category") or user.is_superuser:
            return True     
