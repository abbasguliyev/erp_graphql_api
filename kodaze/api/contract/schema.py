import graphene
from graphene_django.filter import DjangoFilterConnectionField

from . import filters

from .resolvers import (
    resolve_contract,
    resolve_contracts,
    resolve_contract_change,
    resolve_contract_changes,
    resolve_contract_creditor,
    resolve_contract_creditors,
    resolve_contract_gift,
    resolve_contract_gifts,
    resolve_demo_sale,
    resolve_demo_sales,
    resolve_installment,
    resolve_installments
)

from .types import (
    ContractNode,
    ContractChangeNode,
    ContractCreditorNode,
    ContractGiftNode,
    DemoSalesNode,
    InstallmentNode
)
from api.contract.permissions import (
    contract_permissions,
    contract_change_permissions,
    contract_creditor_permissions,
    contract_gift_permissions,
    demo_sales_permissions,
    installment_permissions
)

from django_graphene_permissions import permissions_checker


class ContractQuery(graphene.ObjectType):
    contract = graphene.Field(ContractNode, description="Look up a contract by ID.",
                              id=graphene.Argument(graphene.ID, description="ID for a contract", required=True))

    contracts = DjangoFilterConnectionField(
        ContractNode,
        description="List of contract.",
        filterset_class=filters.ContractFilter,
    )

    @permissions_checker([contract_permissions.ContractReadPermissions])
    def resolve_contract(self, info, **data):
        id = data.get("id")
        return resolve_contract(id)

    @permissions_checker([contract_permissions.ContractReadPermissions])
    def resolve_contracts(self, info, **_kwargs):
        return resolve_contracts()


class ContractChangeQuery(graphene.ObjectType):
    contract_change = graphene.Field(ContractChangeNode, description="Look up a contract change by ID.",
                                     id=graphene.Argument(graphene.ID, description="ID for a contract change", required=True))

    contract_changes = DjangoFilterConnectionField(
        ContractChangeNode,
        description="List of contract change.",
        filterset_class=filters.ContractChangeFilter,
    )

    @permissions_checker([contract_change_permissions.ContractChangeReadPermissions])
    def resolve_contract_change(self, info, **data):
        id = data.get("id")
        return resolve_contract_change(id)

    @permissions_checker([contract_change_permissions.ContractChangeReadPermissions])
    def resolve_contract_changes(self, info, **_kwargs):
        return resolve_contract_changes()


class ContractCreditorQuery(graphene.ObjectType):
    contract_creditor = graphene.Field(ContractCreditorNode, description="Look up a ContractCreditor by ID.",
                                       id=graphene.Argument(graphene.ID, description="ID for a ContractCreditor", required=True))

    contract_creditors = DjangoFilterConnectionField(
        ContractCreditorNode,
        description="List of ContractCreditor.",
        filterset_class=filters.ContractCreditorFilter,
    )

    @permissions_checker([contract_creditor_permissions.ContractCreditorReadPermissions])
    def resolve_contract_creditor(self, info, **data):
        id = data.get("id")
        return resolve_contract_creditor(id)

    @permissions_checker([contract_creditor_permissions.ContractCreditorReadPermissions])
    def resolve_contract_creditors(self, info, **_kwargs):
        return resolve_contract_creditors()


class ContractGiftQuery(graphene.ObjectType):
    contract_gift = graphene.Field(ContractGiftNode, description="Look up a ContractGift by ID.",
                                   id=graphene.Argument(graphene.ID, description="ID for a ContractGift", required=True))

    contract_gifts = DjangoFilterConnectionField(
        ContractGiftNode,
        description="List of ContractGift.",
        filterset_class=filters.ContractGiftFilter,
    )

    @permissions_checker([contract_gift_permissions.ContractGiftReadPermissions])
    def resolve_contract_gift(self, info, **data):
        id = data.get("id")
        return resolve_contract_gift(id)

    @permissions_checker([contract_gift_permissions.ContractGiftReadPermissions])
    def resolve_contract_gifts(self, info, **_kwargs):
        return resolve_contract_gifts()


class DemoSalesQuery(graphene.ObjectType):
    demo_sale = graphene.Field(DemoSalesNode, description="Look up a DemoSales by ID.",
                               id=graphene.Argument(graphene.ID, description="ID for a DemoSales", required=True))

    demo_sales = DjangoFilterConnectionField(
        DemoSalesNode,
        description="List of DemoSales.",
        filterset_class=filters.DemoSalesFilter,
    )

    @permissions_checker([demo_sales_permissions.DemoSalesReadPermissions])
    def resolve_demo_sale(self, info, **data):
        id = data.get("id")
        return resolve_demo_sale(id)

    @permissions_checker([demo_sales_permissions.DemoSalesReadPermissions])
    def resolve_demo_sales(self, info, **_kwargs):
        return resolve_demo_sales()


class InstallmentQuery(graphene.ObjectType):
    installment = graphene.Field(InstallmentNode, description="Look up a Installment by ID.",
                                 id=graphene.Argument(graphene.ID, description="ID for a Installment", required=True))

    installments = DjangoFilterConnectionField(
        InstallmentNode,
        description="List of Installment.",
        filterset_class=filters.InstallmentFilter,
    )

    @permissions_checker([installment_permissions.InstallmentReadPermissions])
    def resolve_installment(self, info, **data):
        id = data.get("id")
        return resolve_installment(id)

    @permissions_checker([installment_permissions.InstallmentReadPermissions])
    def resolve_installments(self, info, **_kwargs):
        return resolve_installments()
