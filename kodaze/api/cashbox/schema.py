import graphene
from graphene_django.filter import DjangoFilterConnectionField

from . import filters

from .resolvers import (
    resolve_cash_flow,
    resolve_cash_flows,
    resolve_company_cashbox,
    resolve_company_cashboxs,
    resolve_holding_cashbox,
    resolve_holding_cashboxs,
    resolve_office_cashbox,
    resolve_office_cashboxs
)

from . types import (
    HoldingCashboxNode,
    CompanyCashboxNode,
    OfficeCashboxNode,
    CashFlowNode
)

from .mutations import (
    company_cashbox_mutations,
    holding_cashbox_mutations,
    office_cashbox_mutations
)

from core.permissions import IsAdminUser
from django_graphene_permissions import permissions_checker
from api.cashbox.permissions import (
    company_cashbox_permissions,
    holding_cashbox_permissions,
    office_cashbox_permissions,
    cash_flow_permissions
)


class HoldingCashboxQuery(graphene.ObjectType):
    holding_cashbox = graphene.Field(HoldingCashboxNode, description="Look up a holding cashbox by ID.",
                                     id=graphene.Argument(graphene.ID, description="ID for a holding cashbox", required=True))

    holding_cashboxs = DjangoFilterConnectionField(
        HoldingCashboxNode,
        description="List of holding cashboxs.",
        filterset_class=filters.HoldingCashboxFilter,
    )

    @permissions_checker([holding_cashbox_permissions.HoldingCashboxReadPermissions])
    def resolve_holding_cashbox(self, info, **data):
        id = data.get("id")
        return resolve_holding_cashbox(id)

    @permissions_checker([holding_cashbox_permissions.HoldingCashboxReadPermissions])
    def resolve_holding_cashboxs(self, info, **_kwargs):
        return resolve_holding_cashboxs()


class CompanyCashboxQuery(graphene.ObjectType):
    company_cashbox = graphene.Field(CompanyCashboxNode, description="Look up a company cashbox by ID.",
                                     id=graphene.Argument(graphene.ID, description="ID for a company cashbox", required=True))

    company_cashboxs = DjangoFilterConnectionField(
        CompanyCashboxNode,
        description="List of company cashboxs.",
        filterset_class=filters.CompanyCashboxFilter,
    )

    @permissions_checker([company_cashbox_permissions.CompanyCashboxReadPermissions])
    def resolve_company_cashbox(self, info, **data):
        id = data.get("id")
        return resolve_company_cashbox(id)

    @permissions_checker([company_cashbox_permissions.CompanyCashboxReadPermissions])
    def resolve_company_cashboxs(self, info, **_kwargs):
        return resolve_company_cashboxs()


class OfficeCashboxQuery(graphene.ObjectType):
    office_cashbox = graphene.Field(OfficeCashboxNode, description="Look up a office cashbox by ID.",
                                    id=graphene.Argument(graphene.ID, description="ID for a office cashbox", required=True))

    office_cashboxs = DjangoFilterConnectionField(
        OfficeCashboxNode,
        description="List of office cashboxs.",
        filterset_class=filters.OfficeCashboxFilter,
    )

    @permissions_checker([office_cashbox_permissions.OfficeCashboxReadPermissions])
    def resolve_office_cashbox(self, info, **data):
        id = data.get("id")
        return resolve_office_cashbox(id)

    @permissions_checker([office_cashbox_permissions.OfficeCashboxReadPermissions])
    def resolve_office_cashboxs(self, info, **_kwargs):
        return resolve_office_cashboxs()

class CashFlowQuery(graphene.ObjectType):
    cash_flow = graphene.Field(CashFlowNode, description="Look up a cash flow by ID.",
                                    id=graphene.Argument(graphene.ID, description="ID for a cash flow", required=True))

    cash_flows = DjangoFilterConnectionField(
        CashFlowNode,
        description="List of cash flows.",
        filterset_class=filters.CashFlowFilter,
    )

    @permissions_checker([cash_flow_permissions.CashFlowReadPermissions])
    def resolve_cash_flow(self, info, **data):
        id = data.get("id")
        return resolve_cash_flow(id)

    @permissions_checker([cash_flow_permissions.CashFlowReadPermissions])
    def resolve_cash_flows(self, info, **_kwargs):
        return resolve_cash_flows()
    
# ----------------------- Mutations ---------------------------------------


class HoldingCashboxMutations(graphene.ObjectType):
    create_holding_cashbox = holding_cashbox_mutations.CreateHoldingCashbox.Field()
    update_holding_cashbox = holding_cashbox_mutations.UpdateHoldingCashbox.Field()
    
class CompanyCashboxMutations(graphene.ObjectType):
    create_company_cashbox = company_cashbox_mutations.CreateCompanyCashbox.Field()
    update_company_cashbox = company_cashbox_mutations.UpdateCompanyCashbox.Field()
    
class OfficeCashboxMutations(graphene.ObjectType):
    create_office_cashbox = office_cashbox_mutations.CreateOfficeCashbox.Field()
    update_office_cashbox = office_cashbox_mutations.UpdateOfficeCashbox.Field()
    