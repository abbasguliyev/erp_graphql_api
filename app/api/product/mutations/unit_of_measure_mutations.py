import graphene
from django_graphene_permissions import permissions_checker
from api.product.types import (
    CreateUnitOfMeasureInput,
    UpdateUnitOfMeasureInput,
    UnitOfMeasureNode
)
from product.models import UnitOfMeasure

from api.product.permissions import (
    unit_of_measure_permissions,
)

class CreateUnitOfMeasure(graphene.Mutation):
    class Arguments:
        input = CreateUnitOfMeasureInput(
            required=True, description="Fields required to create unit of measure"
        )

    unit_of_measure = graphene.Field(UnitOfMeasureNode)
    message = graphene.String()

    class Meta:
        description = "Create new UnitOfMeasure"
        model = UnitOfMeasure

    @permissions_checker([unit_of_measure_permissions.UnitOfMeasureCreatePermissions])
    def mutate(root, info, input):
        unit_of_measure = UnitOfMeasure()
        unit_of_measure.name = input.get("name")
        unit_of_measure.save()

        message = "UnitOfMeasure created"
        return CreateUnitOfMeasure(unit_of_measure=unit_of_measure, message=message)


class UpdateUnitOfMeasure(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True, description="ID of a unit_of_measure")
        input = UpdateUnitOfMeasureInput(
            required=True, description="Fields required to Update unit_of_measure"
        )

    unit_of_measure = graphene.Field(UnitOfMeasureNode)
    message = graphene.String()

    class Meta:
        description = "Update UnitOfMeasure"
        model = UnitOfMeasure

    @permissions_checker([unit_of_measure_permissions.UnitOfMeasureUpdatePermissions])
    def mutate(root, info, input):
        UnitOfMeasure.objects.filter(pk=id).update(**input)
        unit_of_measure = UnitOfMeasure.objects.get(pk=id)
        message = "UnitOfMeasure Updated"
        return UpdateUnitOfMeasure(unit_of_measure=unit_of_measure, message=message)


class DeleteUnitOfMeasure(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True, description="ID of a unit_of_measure")

    message = graphene.String()

    class Meta:
        description = "Delete UnitOfMeasure"
        model = UnitOfMeasure

    @permissions_checker([unit_of_measure_permissions.UnitOfMeasureDeletePermissions])
    def mutate(root, info, id):
        unit_of_measure = UnitOfMeasure.objects.get(pk=id).delete()
        message = "UnitOfMeasure deleted"
        return DeleteUnitOfMeasure(message=message)
