import graphene
from django_graphene_permissions import permissions_checker
from company.models import Company, Holding
from api.company.types import (
    CreateCompanyInput,
    UpdateCompanyInput,
    CompanyNode
)

from api.company.permissions import (
    company_permissions,
)


class CreateCompany(graphene.Mutation):
    class Arguments:
        input = CreateCompanyInput(
            required=True, description="Fields required to create company"
        )

    company = graphene.Field(CompanyNode)
    message = graphene.String()

    class Meta:
        description = "Create new Company"
        model = Company

    @permissions_checker([company_permissions.CompanyCreatePermissions])
    def mutate(root, info, input):
        holding_id = input.get("holding")
        holding = Holding.objects.get(pk=holding_id)
        company = Company()
        company.name = input.get("name")
        company.holding = holding
        company.save()

        message = "Company created"
        return CreateCompany(company=company, message=message)


class UpdateCompany(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True, description="ID of a company")
        input = UpdateCompanyInput(
            required=True, description="Fields required to Update company"
        )

    company = graphene.Field(CompanyNode)
    message = graphene.String()

    class Meta:
        description = "Update Company"
        model = Company

    @permissions_checker([company_permissions.CompanyUpdatePermissions])
    def mutate(root, info, input):
        Company.objects.filter(pk=id).update(**input)
        company = Company.objects.get(pk=id)

        message = "Company Updated"
        return UpdateCompany(company=company, message=message)


class DeleteCompany(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True, description="ID of a company")

    message = graphene.String()

    class Meta:
        description = "Delete Company"
        model = Company

    @permissions_checker([company_permissions.CompanyDeletePermissions])
    def mutate(root, info, id):
        company = Company.objects.get(pk=id)
        company.is_active = False
        company.save()
        message = "Company deactivated"
        return DeleteCompany(message=message)
