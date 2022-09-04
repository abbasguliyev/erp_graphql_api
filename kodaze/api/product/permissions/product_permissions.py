from django_graphene_permissions.permissions import BasePermission

class ProductCreatePermissions(BasePermission):
    @staticmethod
    def has_permission(context):
        user = context.user
        permission_groups = user.groups.all()
        for permission_group in permission_groups:
            all_permissions = permission_group.permissions.all()
            for perm in all_permissions:
                if "add_product" == perm.codename or user.is_superuser:
                    return True

        if user.has_perm("add_product") or user.is_superuser:
            return True

class ProductUpdatePermissions(BasePermission):
    @staticmethod
    def has_permission(context):
        user = context.user
        permission_groups = user.groups.all()
        for permission_group in permission_groups:
            all_permissions = permission_group.permissions.all()
            for perm in all_permissions:
                if "change_product" == perm.codename or user.is_superuser:
                    return True

        if user.has_perm("change_product") or user.is_superuser:
            return True
       
class ProductDeletePermissions(BasePermission):
    @staticmethod
    def has_permission(context):
        user = context.user
        permission_groups = user.groups.all()
        for permission_group in permission_groups:
            all_permissions = permission_group.permissions.all()
            for perm in all_permissions:
                if "delete_product" == perm.codename or user.is_superuser:
                    return True

        if user.has_perm("delete_product") or user.is_superuser:
            return True

class ProductReadPermissions(BasePermission):
    @staticmethod
    def has_permission(context):
        user = context.user
        permission_groups = user.groups.all()
        for permission_group in permission_groups:
            all_permissions = permission_group.permissions.all()
            for perm in all_permissions:
                if "view_product" == perm.codename or user.is_superuser:
                    return True

        if user.has_perm("view_product") or user.is_superuser:
            return True     
