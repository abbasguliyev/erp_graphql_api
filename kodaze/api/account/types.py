from graphene import relay, ObjectType
from graphene_django import DjangoObjectType
from account.models import (
    Customer,
    CustomerNote,
    EmployeeStatus,
    Region,
)
from django.contrib.auth import get_user_model
from . import filters

User = get_user_model()


class CustomerNode(DjangoObjectType):
    class Meta:
        model = Customer
        interfaces = (relay.Node, )


class CustomerNoteNode(DjangoObjectType):
    class Meta:
        model = CustomerNote
        interfaces = (relay.Node, )


class RegionNode(DjangoObjectType):
    class Meta:
        model = Region
        interfaces = (relay.Node, )


class EmployeeStatusNode(DjangoObjectType):
    class Meta:
        model = EmployeeStatus
        interfaces = (relay.Node, )


class UserNode(DjangoObjectType):
    class Meta:
        model = User
        interfaces = (relay.Node, )
