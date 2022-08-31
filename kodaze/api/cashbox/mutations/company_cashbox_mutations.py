import graphene
from django_graphene_permissions import permissions_checker
from core.permissions import IsAdminUser
from company.models import Company
from api.cashbox.types import (
    CreateCompanyCashboxInput,
    UpdateCompanyCashboxInput,
    CompanyCashboxNode
)

from cashbox.models import CompanyCashbox
from api.cashbox.utils import (
    calculate_company_balance,
    calculate_holding_total_balance,
    create_cash_flow
)

from api.cashbox.permissions import (
    company_cashbox_permissions,
)

class CreateCompanyCashbox(graphene.Mutation):
    class Arguments:
        input = CreateCompanyCashboxInput(
            required=True, description="Fields required to create company cashbox"
        )

    company_cashbox = graphene.Field(CompanyCashboxNode)
    message = graphene.String()

    class Meta:
        description = "Create new Company Cahsbox"
        model = CompanyCashbox

    @permissions_checker([company_cashbox_permissions.CompanyCashboxCreatePermissions])
    def mutate(root, info, input):
        initial_balance = calculate_holding_total_balance()
        company_initial_balance = calculate_company_balance()

        company_id = input.get("company")
        company = Company.objects.get(pk=company_id)
        balance = input.get("balance")
        
        company_cashbox = CompanyCashbox()
        company_cashbox.company = company
        company_cashbox.balance = balance
        company_cashbox.save()

        subsequent_balance = calculate_holding_total_balance()
        company_subsequent_balance = calculate_company_balance()

        create_cash_flow(
            company=company,
            description=f"{company.name} şirkət kassasına {float(balance)} AZN əlavə edildi",
            initial_balance=initial_balance,
            subsequent_balance=subsequent_balance,
            company_initial_balance=company_initial_balance,
            company_subsequent_balance=company_subsequent_balance,
            executor=info.context.user,
            quantity=balance
        )

        message = "Company cashbox created"
        return CreateCompanyCashbox(company_cashbox=company_cashbox, message=message)


class UpdateCompanyCashbox(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True, description="ID of a company cashbox")
        input = UpdateCompanyCashboxInput(
            required=True, description="Fields required to Update company cashbox"
        )

    company_cashbox = graphene.Field(CompanyCashboxNode)
    message = graphene.String()

    class Meta:
        description = "Update Company Cahsbox"
        model = CompanyCashbox

    @permissions_checker([company_cashbox_permissions.CompanyCashboxUpdatePermissions])
    def mutate(root, info, input):
        initial_balance = calculate_holding_total_balance()
        company_initial_balance = calculate_company_balance()

        balance = input.get("balance")

        CompanyCashbox.objects.filter(pk=id).update(**input)
        company_cashbox = CompanyCashbox.objects.get(pk=id)

        subsequent_balance = calculate_holding_total_balance()
        company_subsequent_balance = calculate_company_balance()

        create_cash_flow(
            company=company_cashbox.company,
            description=f"{company_cashbox.company.name} şirkət kassasına {float(balance)} AZN əlavə edildi",
            initial_balance=initial_balance,
            subsequent_balance=subsequent_balance,
            company_initial_balance=company_initial_balance,
            company_subsequent_balance=company_subsequent_balance,
            executor=info.context.user,
            quantity=balance
        )
        message = "Company cashbox Updated"
        return UpdateCompanyCashbox(company_cashbox=company_cashbox, message=message)
