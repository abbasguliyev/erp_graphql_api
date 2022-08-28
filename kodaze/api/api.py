import graphene
from .account.schema import (
    CustomerNoteQuery,
    CustomerQuery,
    EmployeeStatusQuery,
    RegionQuery,
    UserQuery
)


class Query(
    CustomerNoteQuery,
    CustomerQuery,
    EmployeeStatusQuery,
    RegionQuery,
    UserQuery
):
    pass


class Mutation(

):
    pass


schema = graphene.Schema(query=Query)
