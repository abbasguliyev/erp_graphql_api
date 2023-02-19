import graphene
from graphene_django.filter import DjangoFilterConnectionField

from . import filters

from .resolvers import (
    resolve_holding,
    resolve_holdings,
    resolve_company,
    resolve_companies,
    resolve_office,
    resolve_offices,
    resolve_department,
    resolve_departments,
    resolve_position,
    resolve_positions,
    resolve_team,
    resolve_teams,
    resolve_permission_for_position,
    resolve_permission_for_positions,
    resolve_app_logo,
    resolve_app_logos
)

from . types import (
    HoldingNode,
    CompanyNode,
    OfficeNode,
    DepartmentNode,
    TeamNode,
    PositionNode,
    AppLogoNode,
    PermissionForPositionNode
)

from .mutations import (
    company_mutations,
    holding_mutations,
    office_mutations,
    department_mutations,
    position_mutations,
    app_logo_mutations,
    permission_for_position_mutations,
    team_mutations,
)

from django_graphene_permissions import permissions_checker
from api.company.permissions import (
    company_permissions,
    holding_permissions,
    office_permissions,
    department_permissions,
    app_logo_permissions,
    permission_for_position_permissions,
    position_permissions,
    team_permissions
)


class HoldingQuery(graphene.ObjectType):
    holding = graphene.Field(HoldingNode, description="Look up a holding by ID.",
                             id=graphene.Argument(graphene.ID, description="ID for a holding", required=True))

    holdings = DjangoFilterConnectionField(
        HoldingNode,
        description="List of holding.",
        filterset_class=filters.HoldingFilter,
    )

    @permissions_checker([holding_permissions.HoldingReadPermissions])
    def resolve_holding(self, info, **data):
        id = data.get("id")
        return resolve_holding(id)

    @permissions_checker([holding_permissions.HoldingReadPermissions])
    def resolve_holdings(self, info, **_kwargs):
        return resolve_holdings()


class CompanyQuery(graphene.ObjectType):
    company = graphene.Field(CompanyNode, description="Look up a company by ID.",
                             id=graphene.Argument(graphene.ID, description="ID for a company", required=True))

    companys = DjangoFilterConnectionField(
        CompanyNode,
        description="List of company.",
        filterset_class=filters.CompanyFilter,
    )

    @permissions_checker([company_permissions.CompanyReadPermissions])
    def resolve_company(self, info, **data):
        id = data.get("id")
        return resolve_company(id)

    @permissions_checker([company_permissions.CompanyReadPermissions])
    def resolve_companys(self, info, **_kwargs):
        return resolve_companies()


class OfficeQuery(graphene.ObjectType):
    office = graphene.Field(OfficeNode, description="Look up a office by ID.",
                            id=graphene.Argument(graphene.ID, description="ID for a office", required=True))

    offices = DjangoFilterConnectionField(
        OfficeNode,
        description="List of office.",
        filterset_class=filters.OfficeFilter,
    )

    @permissions_checker([office_permissions.OfficeReadPermissions])
    def resolve_office(self, info, **data):
        id = data.get("id")
        return resolve_office(id)

    @permissions_checker([office_permissions.OfficeReadPermissions])
    def resolve_offices(self, info, **_kwargs):
        return resolve_offices()


class DepartmentQuery(graphene.ObjectType):
    department = graphene.Field(DepartmentNode, description="Look up a department by ID.",
                                id=graphene.Argument(graphene.ID, description="ID for a department", required=True))

    departments = DjangoFilterConnectionField(
        DepartmentNode,
        description="List of departments.",
        filterset_class=filters.DepartmentFilter,
    )

    @permissions_checker([department_permissions.DepartmentReadPermissions])
    def resolve_department(self, info, **data):
        id = data.get("id")
        return resolve_department(id)

    @permissions_checker([department_permissions.DepartmentReadPermissions])
    def resolve_departments(self, info, **_kwargs):
        return resolve_departments()


class TeamQuery(graphene.ObjectType):
    team = graphene.Field(TeamNode, description="Look up a team by ID.",
                          id=graphene.Argument(graphene.ID, description="ID for a team", required=True))

    teams = DjangoFilterConnectionField(
        TeamNode,
        description="List of teams.",
        filterset_class=filters.TeamFilter,
    )

    @permissions_checker([team_permissions.TeamReadPermissions])
    def resolve_team(self, info, **data):
        id = data.get("id")
        return resolve_team(id)

    @permissions_checker([team_permissions.TeamReadPermissions])
    def resolve_teams(self, info, **_kwargs):
        return resolve_teams()


class PositionQuery(graphene.ObjectType):
    position = graphene.Field(PositionNode, description="Look up a position by ID.",
                              id=graphene.Argument(graphene.ID, description="ID for a position", required=True))

    positions = DjangoFilterConnectionField(
        PositionNode,
        description="List of positions.",
        filterset_class=filters.PositionFilter,
    )

    @permissions_checker([position_permissions.PositionReadPermissions])
    def resolve_position(self, info, **data):
        id = data.get("id")
        return resolve_position(id)

    @permissions_checker([position_permissions.PositionReadPermissions])
    def resolve_positions(self, info, **_kwargs):
        return resolve_positions()


class PermissionForPositionQuery(graphene.ObjectType):
    permission_for_position = graphene.Field(PermissionForPositionNode, description="Look up a permission for position by ID.",
                                             id=graphene.Argument(graphene.ID, description="ID for a permission for position", required=True))

    permission_for_positions = DjangoFilterConnectionField(
        PermissionForPositionNode,
        description="List of permission for positions.",
        filterset_class=filters.PermissionForPositionFilter,
    )

    @permissions_checker([permission_for_position_permissions.PermissionForPositionReadPermissions])
    def resolve_permission_for_position(self, info, **data):
        id = data.get("id")
        return resolve_permission_for_position(id)

    @permissions_checker([permission_for_position_permissions.PermissionForPositionReadPermissions])
    def resolve_permission_for_positions(self, info, **_kwargs):
        return resolve_permission_for_positions()


class AppLogoQuery(graphene.ObjectType):
    app_logo = graphene.Field(AppLogoNode, description="Look up a app logo by ID.",
                              id=graphene.Argument(graphene.ID, description="ID for a app logo", required=True))

    app_logos = DjangoFilterConnectionField(
        AppLogoNode,
        description="List of app logos.",
        filterset_class=filters.AppLogoFilter,
    )

    @permissions_checker([app_logo_permissions.AppLogoReadPermissions])
    def resolve_app_logo(self, info, **data):
        id = data.get("id")
        return resolve_app_logo(id)

    @permissions_checker([app_logo_permissions.AppLogoReadPermissions])
    def resolve_app_logos(self, info, **_kwargs):
        return resolve_app_logos()

# ----------------------- Mutations ---------------------------------------


class HoldingMutations(graphene.ObjectType):
    create_holding = holding_mutations.CreateHolding.Field()
    update_holding = holding_mutations.UpdateHolding.Field()


class CompanyMutations(graphene.ObjectType):
    create_company = company_mutations.CreateCompany.Field()
    update_company = company_mutations.UpdateCompany.Field()
    delete_company = company_mutations.DeleteCompany.Field()


class OfficeMutations(graphene.ObjectType):
    create_office = office_mutations.CreateOffice.Field()
    update_office = office_mutations.UpdateOffice.Field()
    delete_office = office_mutations.DeleteOffice.Field()


class DepartmentMutations(graphene.ObjectType):
    create_department = department_mutations.CreateDepartment.Field()
    update_department = department_mutations.UpdateDepartment.Field()
    delete_department = department_mutations.DeleteDepartment.Field()


class PositionMutations(graphene.ObjectType):
    create_position = position_mutations.CreatePosition.Field()
    update_position = position_mutations.UpdatePosition.Field()
    delete_position = position_mutations.DeletePosition.Field()


class TeamMutations(graphene.ObjectType):
    create_team = team_mutations.CreateTeam.Field()
    update_team = team_mutations.UpdateTeam.Field()
    delete_team = team_mutations.DeleteTeam.Field()


class PermissionForPositionMutations(graphene.ObjectType):
    create_permission_for_position = permission_for_position_mutations.CreatePermissionForPosition.Field()
    update_permission_for_position = permission_for_position_mutations.UpdatePermissionForPosition.Field()
    delete_permission_for_position = permission_for_position_mutations.DeletePermissionForPosition.Field()


class AppLogoMutations(graphene.ObjectType):
    create_app_logo = app_logo_mutations.CreateAppLogo.Field()
    update_app_logo = app_logo_mutations.UpdateAppLogo.Field()
    delete_app_logo = app_logo_mutations.DeleteAppLogo.Field()
