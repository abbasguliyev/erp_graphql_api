from django_graphene_permissions.permissions import BasePermission

class UserCreatePermissions(BasePermission):
    @staticmethod
    def has_permission(context):
        user = context.user
        permission_groups = user.groups.all()
        for permission_group in permission_groups:
            all_permissions = permission_group.permissions.all()
            for perm in all_permissions:
                if "add_user" == perm.codename:
                    return True

        if user.has_perm("add_user"):
            return True

class UserUpdatePermissions(BasePermission):
    @staticmethod
    def has_permission(context):
        user = context.user
        permission_groups = user.groups.all()
        for permission_group in permission_groups:
            all_permissions = permission_group.permissions.all()
            for perm in all_permissions:
                if "change_user" == perm.codename:
                    return True

        if user.has_perm("change_user"):
            return True
       
class UserDeletePermissions(BasePermission):
    @staticmethod
    def has_permission(context):
        user = context.user
        permission_groups = user.groups.all()
        for permission_group in permission_groups:
            all_permissions = permission_group.permissions.all()
            for perm in all_permissions:
                if "delete_user" == perm.codename:
                    return True

        if user.has_perm("delete_user"):
            return True

class UserReadPermissions(BasePermission):
    @staticmethod
    def has_permission(context):
        print(f"*********************{context.user}")
        user = context.user
        permission_groups = user.groups.all()
        for permission_group in permission_groups:
            all_permissions = permission_group.permissions.all()
            for perm in all_permissions:
                if "view_user" == perm.codename:
                    return True

        if user.has_perm("view_user"):
            return True     
