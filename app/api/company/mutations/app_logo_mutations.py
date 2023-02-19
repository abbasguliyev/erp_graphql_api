import graphene
from django_graphene_permissions import permissions_checker
from company.models import AppLogo
from api.company.types import (
    CreateAppLogoInput,
    UpdateAppLogoInput,
    AppLogoNode
)

from api.company.permissions import (
    app_logo_permissions,
)


class CreateAppLogo(graphene.Mutation):
    class Arguments:
        input = CreateAppLogoInput(
            required=True, description="Fields required to create app_logo"
        )

    app_logo = graphene.Field(AppLogoNode)
    message = graphene.String()

    class Meta:
        description = "Create new AppLogo"
        model = AppLogo

    @permissions_checker([app_logo_permissions.AppLogoCreatePermissions])
    def mutate(root, info, input):
        try:
            logo = info.context.FILES[input.get("logo")]
        except:
            logo = None

        app_logo = AppLogo()
        app_logo.logo = logo
        app_logo.save()
        message = "AppLogo created"
        return CreateAppLogo(app_logo=app_logo, message=message)


class UpdateAppLogo(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True, description="ID of a app_logo")
        input = UpdateAppLogoInput(
            required=True, description="Fields required to Update app_logo"
        )

    app_logo = graphene.Field(AppLogoNode)
    message = graphene.String()

    class Meta:
        description = "Update AppLogo"
        model = AppLogo

    @permissions_checker([app_logo_permissions.AppLogoUpdatePermissions])
    def mutate(root, info, input):
        AppLogo.objects.filter(pk=id).update(**input)
        app_logo = AppLogo.objects.get(pk=id)
        message = "AppLogo Updated"
        return UpdateAppLogo(app_logo=app_logo, message=message)


class DeleteAppLogo(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True, description="ID of a app_logo")

    message = graphene.String()

    class Meta:
        description = "Delete AppLogo"
        model = AppLogo

    @permissions_checker([app_logo_permissions.AppLogoDeletePermissions])
    def mutate(root, info, id):
        AppLogo.objects.get(pk=id).delete()
        message = "AppLogo deleted"
        return DeleteAppLogo(message=message)
