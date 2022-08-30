import graphene
import graphql_jwt
from .account.schema import (
    CustomerMutations,
    CustomerNoteQuery,
    CustomerNoteMutations,
    EmployeeStatusMutations,
    RegionMutations,
    UserMutations,
    CustomerQuery,
    EmployeeStatusQuery,
    RegionQuery,
    UserQuery,
    PermissionQuery,
    GroupQuery,
)

from graphql_auth.schema import UserQuery as GUserQuery, MeQuery


class Query(
    CustomerNoteQuery,
    CustomerQuery,
    EmployeeStatusQuery,
    RegionQuery,
    UserQuery,
    PermissionQuery,
    GroupQuery,
    GUserQuery, 
    MeQuery
):
    pass


class Mutation(
    CustomerMutations,
    CustomerNoteMutations,
    EmployeeStatusMutations,
    RegionMutations,
    UserMutations,
):
   pass


schema = graphene.Schema(query=Query, mutation=Mutation)
