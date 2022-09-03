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
from .cashbox.schema import (
    CashFlowQuery,
    CompanyCashboxQuery,
    HoldingCashboxQuery,
    OfficeCashboxQuery,
    HoldingCashboxMutations,
    CompanyCashboxMutations,
    OfficeCashboxMutations
)

from .company.schema import (
    HoldingQuery,
    OfficeQuery,
    CompanyQuery,
    DepartmentQuery,
    TeamQuery,
    PositionQuery,
    PermissionForPositionQuery,
    AppLogoQuery,
    HoldingMutations,
    CompanyMutations,
    OfficeMutations,
    DepartmentMutations,
    PermissionForPositionMutations,
    TeamMutations,
    AppLogoMutations,
    PositionMutations
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
    CashFlowQuery,
    CompanyCashboxQuery,
    HoldingCashboxQuery,
    OfficeCashboxQuery,
    HoldingQuery,
    OfficeQuery,
    CompanyQuery,
    DepartmentQuery,
    TeamQuery,
    PositionQuery,
    PermissionForPositionQuery,
    AppLogoQuery,
):
    pass


class Mutation(
    CustomerMutations,
    CustomerNoteMutations,
    EmployeeStatusMutations,
    RegionMutations,
    UserMutations,
    BackupAndRestoreMutations,
    HoldingCashboxMutations,
    CompanyCashboxMutations,
    OfficeCashboxMutations,
    HoldingMutations,
    CompanyMutations,
    OfficeMutations,
    DepartmentMutations,
    PermissionForPositionMutations,
    TeamMutations,
    AppLogoMutations,
    PositionMutations
):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
