import graphene
from django_graphene_permissions import permissions_checker
from api.company.types import (
    CreateHoldingInput,
    UpdateHoldingInput,
    HoldingNode
)

from company.models import Holding

from api.company.permissions import (
    holding_permissions,
)

class CreateHolding(graphene.Mutation):
    class Arguments:
        input = CreateHoldingInput(
            required=True, description="Fields required to create holding"
        )

    holding = graphene.Field(HoldingNode)
    message = graphene.String()

    class Meta:
        description = "Create new Holding"
        model = Holding

    @permissions_checker([holding_permissions.HoldingCreatePermissions])
    def mutate(root, info, input):
        holding = Holding()
        holding.name = input.get("name")
        holding.save()

        message = "Holding created"
        return CreateHolding(holding=holding, message=message)


class UpdateHolding(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True, description="ID of a holding")
        input = UpdateHoldingInput(
            required=True, description="Fields required to Update holding"
        )

    holding = graphene.Field(HoldingNode)
    message = graphene.String()

    class Meta:
        description = "Update Holding"
        model = Holding

    @permissions_checker([holding_permissions.HoldingUpdatePermissions])
    def mutate(root, info, input):
        Holding.objects.filter(pk=id).update(**input)
        holding = Holding.objects.get(pk=id)
        message = "Holding Updated"
        return UpdateHolding(holding=holding, message=message)
