import graphene
from django_graphene_permissions import permissions_checker
from core.permissions import IsAdminUser
from company.models import Holding
from api.cashbox.types import (
    CreateHoldingCashboxInput,
    UpdateHoldingCashboxInput,
    HoldingCashboxNode
)

from cashbox.models import HoldingCashbox
from api.cashbox.utils import (
    calculate_holding_total_balance,
    calculate_holding_balance,
    create_cash_flow
)
from api.cashbox.permissions import (
    holding_cashbox_permissions,
)

class CreateHoldingCashbox(graphene.Mutation):
    class Arguments:
        input = CreateHoldingCashboxInput(
            required=True, description="Fields required to create holding cashbox"
        )

    holding_cashbox = graphene.Field(HoldingCashboxNode)
    message = graphene.String()

    class Meta:
        description = "Create new Holding Cahsbox"
        model = HoldingCashbox

    @permissions_checker([holding_cashbox_permissions.HoldingCashboxCreatePermissions])
    def mutate(root, info, input):
        initial_balance = calculate_holding_total_balance()
        holding_initial_balance = calculate_holding_balance()

        holding_id = input.get("holding")
        holding = Holding.objects.get(pk=holding_id)
        balance = input.get("balance")

        holding_cashbox = HoldingCashbox()
        holding_cashbox.holding = holding
        holding_cashbox.balance = balance
        holding_cashbox.save()

        subsequent_balance = calculate_holding_total_balance()
        holding_subsequent_balance = calculate_holding_balance()

        create_cash_flow(
            holding=holding,
            description=f"{holding.name} holdinq cashboxsına {float(balance)} AZN əlavə edildi",
            initial_balance=initial_balance,
            subsequent_balance=subsequent_balance,
            holding_initial_balance=holding_initial_balance,
            holding_subsequent_balance=holding_subsequent_balance,
            executor=info.context.user,
            quantity=balance
        )

        message = "Holding cashbox created"
        return CreateHoldingCashbox(holding_cashbox=holding_cashbox, message=message)


class UpdateHoldingCashbox(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True, description="ID of a holding cashbox")
        input = UpdateHoldingCashboxInput(
            required=True, description="Fields required to Update holding cashbox"
        )

    holding_cashbox = graphene.Field(HoldingCashboxNode)
    message = graphene.String()

    class Meta:
        description = "Update Holding Cahsbox"
        model = HoldingCashbox

    @permissions_checker([holding_cashbox_permissions.HoldingCashboxUpdatePermissions])
    def mutate(root, info, input):
        initial_balance = calculate_holding_total_balance()
        holding_initial_balance = calculate_holding_balance()

        balance = input.get("balance")

        HoldingCashbox.objects.filter(pk=id).update(**input)
        holding_cashbox = HoldingCashbox.objects.get(pk=id)

        subsequent_balance = calculate_holding_total_balance()
        holding_subsequent_balance = calculate_holding_balance()

        create_cash_flow(
            holding=holding_cashbox.holding,
            description=f"{holding_cashbox.holding.name} holdinq cashboxsına {float(balance)} AZN əlavə edildi",
            initial_balance=initial_balance,
            subsequent_balance=subsequent_balance,
            holding_initial_balance=holding_initial_balance,
            holding_subsequent_balance=holding_subsequent_balance,
            executor=info.context.user,
            quantity=balance
        )
        message = "Holding cashbox Updated"
        return UpdateHoldingCashbox(holding_cashbox=holding_cashbox, message=message)
