import graphene
from django_graphene_permissions import permissions_checker
from company.models import Company, Office
from api.company.types import (
    CreateOfficeInput,
    UpdateOfficeInput,
    OfficeNode
)

from api.company.permissions import (
    office_permissions,
)


class CreateOffice(graphene.Mutation):
    class Arguments:
        input = CreateOfficeInput(
            required=True, description="Fields required to create office"
        )

    office = graphene.Field(OfficeNode)
    message = graphene.String()

    class Meta:
        description = "Create new Office"
        model = Office

    @permissions_checker([office_permissions.OfficeCreatePermissions])
    def mutate(root, info, input):
        company_id = input.get("company")
        company = Company.objects.get(pk=company_id)
        office = Office()
        office.name = input.get("name")
        office.company = company
        office.save()
        message = "Office created"
        return CreateOffice(office=office, message=message)


class UpdateOffice(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True, description="ID of a office")
        input = UpdateOfficeInput(
            required=True, description="Fields required to Update office"
        )

    office = graphene.Field(OfficeNode)
    message = graphene.String()

    class Meta:
        description = "Update Office"
        model = Office

    @permissions_checker([office_permissions.OfficeUpdatePermissions])
    def mutate(root, info, input):
        Office.objects.filter(pk=id).update(**input)
        office = Office.objects.get(pk=id)
        message = "Office Updated"
        return UpdateOffice(office=office, message=message)


class DeleteOffice(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True, description="ID of a office")

    message = graphene.String()

    class Meta:
        description = "Delete Office"
        model = Office

    @permissions_checker([office_permissions.OfficeDeletePermissions])
    def mutate(root, info, id):
        office = Office.objects.get(pk=id)
        office.is_active = False
        office.save()
        message = "Office deactivated"
        return DeleteOffice(message=message)
