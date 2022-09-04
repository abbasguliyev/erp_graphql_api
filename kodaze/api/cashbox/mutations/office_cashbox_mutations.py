import graphene
from django_graphene_permissions import permissions_checker
from core.permissions import IsAdminUser
from company.models import Office
from api.cashbox.types import (
    CreateOfficeCashboxInput,
    UpdateOfficeCashboxInput,
    OfficeCashboxNode
)

from cashbox.models import OfficeCashbox
from api.cashbox.utils import (
    calculate_office_balance,
    calculate_holding_total_balance,
    create_cash_flow
)


from api.cashbox.permissions import (
    office_cashbox_permissions,
)


class CreateOfficeCashbox(graphene.Mutation):
    class Arguments:
        input = CreateOfficeCashboxInput(
            required=True, description="Fields required to create office cashbox"
        )

    office_cashbox = graphene.Field(OfficeCashboxNode)
    message = graphene.String()

    class Meta:
        description = "Create new Office Cahsbox"
        model = OfficeCashbox

    @permissions_checker([office_cashbox_permissions.OfficeCashboxCreatePermissions])
    def mutate(root, info, input):
        initial_balance = calculate_holding_total_balance()
        office_initial_balance = calculate_office_balance()

        office_id = input.get("office")
        office = Office.objects.get(pk=office_id)
        balance = input.get("balance")

        office_cashbox = OfficeCashbox()
        office_cashbox.office = office
        office_cashbox.balance = balance
        office_cashbox.save()

        subsequent_balance = calculate_holding_total_balance()
        office_subsequent_balance = calculate_office_balance()

        create_cash_flow(
            office=office,
            description=f"{office.name} ofis cashboxsına {float(balance)} AZN əlavə edildi",
            initial_balance=initial_balance,
            subsequent_balance=subsequent_balance,
            office_initial_balance=office_initial_balance,
            office_subsequent_balance=office_subsequent_balance,
            executor=info.context.user,
            quantity=balance
        )

        message = "Office cashbox created"
        return CreateOfficeCashbox(office_cashbox=office_cashbox, message=message)


class UpdateOfficeCashbox(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True, description="ID of a office cashbox")
        input = UpdateOfficeCashboxInput(
            required=True, description="Fields required to Update office cashbox"
        )

    office_cashbox = graphene.Field(OfficeCashboxNode)
    message = graphene.String()

    class Meta:
        description = "Update Office Cahsbox"
        model = OfficeCashbox

    @permissions_checker([office_cashbox_permissions.OfficeCashboxUpdatePermissions])
    def mutate(root, info, input):
        initial_balance = calculate_holding_total_balance()
        office_initial_balance = calculate_office_balance()

        balance = input.get("balance")

        OfficeCashbox.objects.filter(pk=id).update(**input)
        office_cashbox = OfficeCashbox.objects.get(pk=id)

        subsequent_balance = calculate_holding_total_balance()
        office_subsequent_balance = calculate_office_balance()

        create_cash_flow(
            office=office_cashbox.office,
            description=f"{office_cashbox.office.name} şirkət cashboxsına {float(balance)} AZN əlavə edildi",
            initial_balance=initial_balance,
            subsequent_balance=subsequent_balance,
            office_initial_balance=office_initial_balance,
            office_subsequent_balance=office_subsequent_balance,
            executor=info.context.user,
            quantity=balance
        )
        message = "Office cashbox Updated"
        return UpdateOfficeCashbox(office_cashbox=office_cashbox, message=message)
