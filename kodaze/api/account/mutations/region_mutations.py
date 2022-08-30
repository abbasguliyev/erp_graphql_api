import graphene

from api.account.types import (
    CreateRegionInput,
    RegionNode,
    UpdateRegionInput,
)

from account.models import (
    Region,
)

from django_graphene_permissions import permissions_checker
from account.permissions.region_permissions import (
    RegionCreatePermissions,
    RegionUpdatePermissions,
    RegionDeletePermissions
)

import json
import os
from core.settings import BASE_DIR
from core.permissions import IsAdminUser


class CreateRegion(graphene.Mutation):
    class Arguments:
        input = CreateRegionInput(
            required=True, description="Fields required to create region"
        )

    region = graphene.Field(RegionNode)
    message = graphene.String()

    class Meta:
        description = "Create new Region"
        model = Region

    @permissions_checker([RegionCreatePermissions])
    def mutate(root, info, input):
        region = Region()
        region.region_name = input.get("region_name")
        region.save()
        message = "Region created"
        return CreateRegion(region=region, message=message)


class UpdateRegion(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True, description="ID of a region")
        input = UpdateRegionInput(
            required=True, description="Fields required to Update region")

    region = graphene.Field(RegionNode)
    message = graphene.String()

    class Meta:
        description = "Update Region"
        model = Region

    @permissions_checker([RegionUpdatePermissions])
    def mutate(root, info, input, id):
        Region.objects.filter(pk=id).update(**input)
        region = Region.objects.get(pk=id)
        message = "Region updated"
        return UpdateRegion(region=region, message=message)


class DeleteRegion(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True, description="ID of a region")

    class Meta:
        description = "Delete Region"
        model = Region
    message = graphene.String()

    @permissions_checker([RegionDeletePermissions])
    def mutate(root, info, id):
        region = Region.objects.get(pk=id).delete()
        message = "Region deleted"
        return DeleteRegion(message=message)


class AllRegionCreate(graphene.Mutation):
    class Meta:
        description = "Create All Region"
        model = Region
    message = graphene.String()

    @permissions_checker([IsAdminUser])
    def mutate(cls, root, info, id):
        filename = os.path.join(BASE_DIR, 'cities.json')
        with open(filename) as fp:
            cities = json.load(fp)
        for city in cities:
            regions = Region.objects.filter(region_name=city['name'])
            if len(regions) > 0:
                continue
            region = Region.objects.create(region_name=city['name'])
            region.save()
        message = "All region created"
        return AllRegionCreate(message=message)
