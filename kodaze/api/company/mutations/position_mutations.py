import graphene
from django_graphene_permissions import permissions_checker
from company.models import Position
from api.company.types import (
    CreatePositionInput,
    UpdatePositionInput,
    PositionNode
)

from api.company.permissions import (
    position_permissions,
)


class CreatePosition(graphene.Mutation):
    class Arguments:
        input = CreatePositionInput(
            required=True, description="Fields required to create position"
        )

    position = graphene.Field(PositionNode)
    message = graphene.String()

    class Meta:
        description = "Create new Position"
        model = Position

    @permissions_checker([position_permissions.PositionCreatePermissions])
    def mutate(root, info, input):
        position = Position()
        position.name = input.get("name")
        position.save()
        message = "Position created"
        return CreatePosition(position=position, message=message)


class UpdatePosition(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True, description="ID of a position")
        input = UpdatePositionInput(
            required=True, description="Fields required to Update position"
        )

    position = graphene.Field(PositionNode)
    message = graphene.String()

    class Meta:
        description = "Update Position"
        model = Position

    @permissions_checker([position_permissions.PositionUpdatePermissions])
    def mutate(root, info, input):
        Position.objects.filter(pk=id).update(**input)
        position = Position.objects.get(pk=id)
        message = "Position Updated"
        return UpdatePosition(position=position, message=message)


class DeletePosition(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True, description="ID of a position")

    message = graphene.String()

    class Meta:
        description = "Delete Position"
        model = Position

    @permissions_checker([position_permissions.PositionDeletePermissions])
    def mutate(root, info, id):
        position = Position.objects.get(pk=id)
        position.is_active = False
        position.save()
        message = "Position deactivated"
        return DeletePosition(message=message)
