import graphene
from graphene import relay, InputObjectType
from graphene_django import DjangoObjectType
from cashbox.models import (
    HoldingCashbox,
    CompanyCashbox,
    OfficeCashbox,
    CashFlow
)


class HoldingCashboxNode(DjangoObjectType):
    class Meta:
        model = HoldingCashbox
        interfaces = (relay.Node, )


class CompanyCashboxNode(DjangoObjectType):
    class Meta:
        model = CompanyCashbox
        interfaces = (relay.Node, )


class OfficeCashboxNode(DjangoObjectType):
    class Meta:
        model = OfficeCashbox
        interfaces = (relay.Node, )


class CashFlowNode(DjangoObjectType):
    class Meta:
        model = CashFlow
        interfaces = (relay.Node, )


class CreateHoldingCashboxInput(InputObjectType):
    holding = graphene.ID(required=True, default=None,
                          description="holding")

    balance = graphene.Decimal(required=True, description="balance")
    
class UpdateHoldingCashboxInput(InputObjectType):
    holding = graphene.ID(required=False, default=None,
                          description="holding")

    balance = graphene.Decimal(required=False, description="balance")
    
class CreateCompanyCashboxInput(InputObjectType):
    company = graphene.ID(required=True, default=None,
                          description="company")

    balance = graphene.Decimal(required=True, description="balance")
    
class UpdateCompanyCashboxInput(InputObjectType):
    company = graphene.ID(required=False, default=None,
                          description="company")

    balance = graphene.Decimal(required=False, description="balance")
           
class CreateOfficeCashboxInput(InputObjectType):
    office = graphene.ID(required=True, default=None,
                          description="office")

    balance = graphene.Decimal(required=True, description="balance")
    
class UpdateOfficeCashboxInput(InputObjectType):
    office = graphene.ID(required=False, default=None,
                          description="office")

    balance = graphene.Decimal(required=False, description="balance")
