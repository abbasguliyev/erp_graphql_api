from django_graphene_permissions.permissions import BasePermission

class CustomerNoteCreatePermissions(BasePermission):
    @staticmethod
    def has_permission(context):
        user = context.user
        permission_groups = user.groups.all()
        for permission_group in permission_groups:
            all_permissions = permission_group.permissions.all()
            for perm in all_permissions:
                if "add_customernote" == perm.codename:
                    return True

        if user.has_perm("add_customernote"):
            return True

class CustomerNoteUpdatePermissions(BasePermission):
    @staticmethod
    def has_permission(context):
        user = context.user
        permission_groups = user.groups.all()
        for permission_group in permission_groups:
            all_permissions = permission_group.permissions.all()
            for perm in all_permissions:
                if "change_customernote" == perm.codename:
                    return True

        if user.has_perm("change_customernote"):
            return True
       
class CustomerNoteDeletePermissions(BasePermission):
    @staticmethod
    def has_permission(context):
        user = context.user
        permission_groups = user.groups.all()
        for permission_group in permission_groups:
            all_permissions = permission_group.permissions.all()
            for perm in all_permissions:
                if "delete_customernote" == perm.codename:
                    return True

        if user.has_perm("delete_customernote"):
            return True

class CustomerNoteReadPermissions(BasePermission):
    @staticmethod
    def has_permission(context):
        user = context.user
        permission_groups = user.groups.all()
        for permission_group in permission_groups:
            all_permissions = permission_group.permissions.all()
            for perm in all_permissions:
                if "view_customernote" == perm.codename:
                    return True

        if user.has_perm("view_customernote"):
            return True     
