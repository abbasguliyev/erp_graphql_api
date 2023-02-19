import graphene
from django_graphene_permissions import permissions_checker
from company.models import PermissionForPosition
from api.company.types import (
    CreatePermissionForPositionInput,
    UpdatePermissionForPositionInput,
    PermissionForPositionNode
)

from api.company.permissions import (
    permission_for_position_permissions,
)


class CreatePermissionForPosition(graphene.Mutation):
    class Arguments:
        input = CreatePermissionForPositionInput(
            required=True, description="Fields required to create permission_for_position"
        )

    permission_for_position = graphene.Field(PermissionForPositionNode)
    message = graphene.String()

    class Meta:
        description = "Create new PermissionForPosition"
        model = PermissionForPosition

    @permissions_checker([permission_for_position_permissions.PermissionForPositionCreatePermissions])
    def mutate(root, info, input):
        permission_for_position = PermissionForPosition()
        permission_for_position.position = input.get("position")
        permission_for_position.permission_group = input.get(
            "permission_group")
        permission_for_position.save()
        message = "PermissionForPosition created"
        return CreatePermissionForPosition(permission_for_position=permission_for_position, message=message)


class UpdatePermissionForPosition(graphene.Mutation):
    class Arguments:
        id = graphene.ID(
            required=True, description="ID of a permission_for_position")
        input = UpdatePermissionForPositionInput(
            required=True, description="Fields required to Update permission_for_position"
        )

    permission_for_position = graphene.Field(PermissionForPositionNode)
    message = graphene.String()

    class Meta:
        description = "Update PermissionForPosition"
        model = PermissionForPosition

    @permissions_checker([permission_for_position_permissions.PermissionForPositionUpdatePermissions])
    def mutate(root, info, input):
        PermissionForPosition.objects.filter(pk=id).update(**input)
        permission_for_position = PermissionForPosition.objects.get(pk=id)
        message = "PermissionForPosition Updated"
        return UpdatePermissionForPosition(permission_for_position=permission_for_position, message=message)


class DeletePermissionForPosition(graphene.Mutation):
    class Arguments:
        id = graphene.ID(
            required=True, description="ID of a permission_for_position")

    message = graphene.String()

    class Meta:
        description = "Delete PermissionForPosition"
        model = PermissionForPosition

    @permissions_checker([permission_for_position_permissions.PermissionForPositionDeletePermissions])
    def mutate(root, info, id):
        PermissionForPosition.objects.get(pk=id).delete()
        message = "PermissionForPosition deleted"
        return DeletePermissionForPosition(message=message)
