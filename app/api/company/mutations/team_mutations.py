import graphene
from django_graphene_permissions import permissions_checker
from company.models import Team
from api.company.types import (
    CreateTeamInput,
    UpdateTeamInput,
    TeamNode
)

from api.company.permissions import (
    team_permissions,
)


class CreateTeam(graphene.Mutation):
    class Arguments:
        input = CreateTeamInput(
            required=True, description="Fields required to create team"
        )

    team = graphene.Field(TeamNode)
    message = graphene.String()

    class Meta:
        description = "Create new Team"
        model = Team

    @permissions_checker([team_permissions.TeamCreatePermissions])
    def mutate(root, info, input):
        team = Team()
        team.name = input.get("name")
        team.save()
        message = "Team created"
        return CreateTeam(team=team, message=message)


class UpdateTeam(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True, description="ID of a team")
        input = UpdateTeamInput(
            required=True, description="Fields required to Update team"
        )

    team = graphene.Field(TeamNode)
    message = graphene.String()

    class Meta:
        description = "Update Team"
        model = Team

    @permissions_checker([team_permissions.TeamUpdatePermissions])
    def mutate(root, info, input):
        Team.objects.filter(pk=id).update(**input)
        team = Team.objects.get(pk=id)
        message = "Team Updated"
        return UpdateTeam(team=team, message=message)


class DeleteTeam(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True, description="ID of a team")

    message = graphene.String()

    class Meta:
        description = "Delete Team"
        model = Team

    @permissions_checker([team_permissions.TeamDeletePermissions])
    def mutate(root, info, id):
        team = Team.objects.get(pk=id)
        team.is_active = False
        team.save()
        message = "Team deactivated"
        return DeleteTeam(message=message)
