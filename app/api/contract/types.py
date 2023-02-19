import graphene
from graphene import relay, InputObjectType
from graphene_django import DjangoObjectType

from contract.models import (
    Installment,
    Contract,
    ContractChange,
    ContractCreditor,
    ContractGift,
    DemoSales
)


class ContractNode(DjangoObjectType):
    class Meta:
        model = Contract
        interfaces = (relay.Node, )


class InstallmentNode(DjangoObjectType):
    class Meta:
        model = Installment
        interfaces = (relay.Node, )


class ContractChangeNode(DjangoObjectType):
    class Meta:
        model = ContractChange
        interfaces = (relay.Node, )


class ContractCreditorNode(DjangoObjectType):
    class Meta:
        model = ContractCreditor
        interfaces = (relay.Node, )


class ContractGiftNode(DjangoObjectType):
    class Meta:
        model = ContractGift
        interfaces = (relay.Node, )


class DemoSalesNode(DjangoObjectType):
    class Meta:
        model = DemoSales
        interfaces = (relay.Node, )

