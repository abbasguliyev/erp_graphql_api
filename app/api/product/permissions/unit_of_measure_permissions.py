from django_graphene_permissions.permissions import BasePermission

class UnitOfMeasureCreatePermissions(BasePermission):
    @staticmethod
    def has_permission(context):
        user = context.user
        permission_groups = user.groups.all()
        for permission_group in permission_groups:
            all_permissions = permission_group.permissions.all()
            for perm in all_permissions:
                if "add_unitofmeasure" == perm.codename or user.is_superuser:
                    return True

        if user.has_perm("add_unitofmeasure") or user.is_superuser:
            return True

class UnitOfMeasureUpdatePermissions(BasePermission):
    @staticmethod
    def has_permission(context):
        user = context.user
        permission_groups = user.groups.all()
        for permission_group in permission_groups:
            all_permissions = permission_group.permissions.all()
            for perm in all_permissions:
                if "change_unitofmeasure" == perm.codename or user.is_superuser:
                    return True

        if user.has_perm("change_unitofmeasure") or user.is_superuser:
            return True
       
class UnitOfMeasureDeletePermissions(BasePermission):
    @staticmethod
    def has_permission(context):
        user = context.user
        permission_groups = user.groups.all()
        for permission_group in permission_groups:
            all_permissions = permission_group.permissions.all()
            for perm in all_permissions:
                if "delete_unitofmeasure" == perm.codename or user.is_superuser:
                    return True

        if user.has_perm("delete_unitofmeasure") or user.is_superuser:
            return True

class UnitOfMeasureReadPermissions(BasePermission):
    @staticmethod
    def has_permission(context):
        user = context.user
        permission_groups = user.groups.all()
        for permission_group in permission_groups:
            all_permissions = permission_group.permissions.all()
            for perm in all_permissions:
                if "view_unitofmeasure" == perm.codename or user.is_superuser:
                    return True

        if user.has_perm("view_unitofmeasure") or user.is_superuser:
            return True     
