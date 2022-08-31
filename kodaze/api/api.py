import graphene
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
from .backup_restore.schema import (
    BackupAndRestoreMutations,
    BackupAndRestoreQuery
)

from graphql_auth.schema import MeQuery


class Query(
    CustomerNoteQuery,
    CustomerQuery,
    EmployeeStatusQuery,
    RegionQuery,
    UserQuery,
    PermissionQuery,
    GroupQuery,
    MeQuery,
    BackupAndRestoreQuery,
):
    pass


class Mutation(
    CustomerMutations,
    CustomerNoteMutations,
    EmployeeStatusMutations,
    RegionMutations,
    UserMutations,
    BackupAndRestoreMutations,
):
   pass


schema = graphene.Schema(query=Query, mutation=Mutation)
