import graphene
from graphene import relay, InputObjectType
from graphene_django import DjangoObjectType
from company.models import (
    Company,
    Holding,
    Office,
    Team,
    Department,
    PermissionForPosition,
    Position,
    AppLogo
)
from api.account.types import GroupNode
from api.core import values


class HoldingNode(DjangoObjectType):
    class Meta:
        model = Holding
        interfaces = (relay.Node, )


class CompanyNode(DjangoObjectType):
    class Meta:
        model = Company
        interfaces = (relay.Node, )


class OfficeNode(DjangoObjectType):
    class Meta:
        model = Office
        interfaces = (relay.Node, )


class DepartmentNode(DjangoObjectType):
    class Meta:
        model = Department
        interfaces = (relay.Node, )


class TeamNode(DjangoObjectType):
    class Meta:
        model = Team
        interfaces = (relay.Node, )


class PermissionForPositionNode(DjangoObjectType):
    class Meta:
        model = PermissionForPosition
        interfaces = (relay.Node, )


class PositionNode(DjangoObjectType):
    class Meta:
        model = Position
        interfaces = (relay.Node, )


class AppLogoNode(DjangoObjectType):
    class Meta:
        model = AppLogo
        interfaces = (relay.Node, )


class CreateHoldingInput(InputObjectType):
    name = graphene.String(required=True, description="holding name")


class UpdateHoldingInput(InputObjectType):
    name = graphene.String(required=False, description="holding name")
    is_active = graphene.Boolean(
        required=False, description="holding is active")


class CreateCompanyInput(InputObjectType):
    name = graphene.String(required=True, description="company name")
    holding = graphene.ID(HoldingNode, required=True, description = "company holding")


class UpdateCompanyInput(InputObjectType):
    name = graphene.String(required=False, description="company name")
    is_active = graphene.Boolean(
        required=False, description="company is active")


class CreateOfficeInput(InputObjectType):
    name = graphene.String(required=True, description="office name")
    company = graphene.ID(CompanyNode, required=True, description = "office company")


class UpdateOfficeInput(InputObjectType):
    name = graphene.String(required=False, description="office name")
    is_active = graphene.Boolean(
        required=False, description="office is active")


class CreateDepartmentInput(InputObjectType):
    name = graphene.String(required=True, description="department name")
    office = graphene.ID(OfficeNode, required=True, description = "department office")
    


class UpdateDepartmentInput(InputObjectType):
    name = graphene.String(required=False, description="department name")
    is_active = graphene.Boolean(
        required=False, description="department is active")


class CreateTeamInput(InputObjectType):
    name = graphene.String(required=True, description="team name")


class UpdateTeamInput(InputObjectType):
    name = graphene.String(required=False, description="team name")
    is_active = graphene.Boolean(
        required=False, description="team is active")


class CreatePositionInput(InputObjectType):
    name = graphene.String(required=True, description="position name")


class UpdatePositionInput(InputObjectType):
    name = graphene.String(required=False, description="position name")
    is_active = graphene.Boolean(
        required=False, description="position is active")


class CreatePermissionForPositionInput(InputObjectType):
    position = graphene.ID(PositionNode, required=True, description="position")
    permission_group = graphene.ID(
        GroupNode, required=True, description="group")


class UpdatePermissionForPositionInput(InputObjectType):
    position = graphene.ID(PositionNode, required=False,
                           description="position")
    permission_group = graphene.ID(
        GroupNode, required=False, description="group")


class CreateAppLogoInput(InputObjectType):
    logo = values.Upload(required=True, description="Logo")


class UpdateAppLogoInput(InputObjectType):
    logo = values.Upload(required=True, description="Logo")

