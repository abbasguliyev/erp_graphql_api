import graphene
from graphene_django.filter import DjangoFilterConnectionField
from . import filters
from .resolvers import (
    resolve_customers,
    resolve_cutomer,
    resolve_cutomer_notes,
    resolve_cutomer_note,
    resolve_employee_status,
    resolve_employee_statuses,
    resolve_regions,
    resolve_region,
    resolve_users,
    resolve_user
)
from .types import (
    CustomerNode,
    CustomerNoteNode,
    EmployeeStatusNode,
    RegionNode,
    UserNode
)

from . import filters

class CustomerQuery(graphene.ObjectType):
    customer = graphene.Field(
        CustomerNode,
        description = "Look up a customer by ID.",
        id = graphene.Argument(graphene.ID, description="ID for a customer", required=True)
    )
    all_customers = DjangoFilterConnectionField(
        CustomerNode,
        description = "List of customers.",
        filterset_class=filters.CustomerFilter,
    )

    def resolve_customer(self, info, **data):
        id = data.get("id")
        return resolve_cutomer(id)
    
    def resolve_customers(self, info, **_kwargs):
        return resolve_customers()
    
    
    
class CustomerNoteQuery(graphene.ObjectType):
    customer_note = graphene.Field(
        CustomerNoteNode,
        description = "Look up a customer note by ID.",
        id = graphene.Argument(graphene.ID, description="ID for a customer note", required=True)
    )
    all_customer_notes = DjangoFilterConnectionField(
        CustomerNoteNode,
        description = "List of customer notes.",
        filterset_class=filters.CustomerNoteFilter,
    )
    
    def resolve_customer_note(self, info, **data):
        id = data.get("id")
        return resolve_cutomer_note(id)
    
    def resolve_customer_notes(self, info, **_kwargs):
        return resolve_cutomer_notes()


class EmployeeStatusQuery(graphene.ObjectType):
    employee_status = graphene.Field(
        EmployeeStatusNode,
        description = "Look up a employee status by ID.",
        id = graphene.Argument(graphene.ID, description="ID for a employee status", required=True)
    )
    all_employee_statuses = DjangoFilterConnectionField(
        EmployeeStatusNode,
        description = "List of employee statuses.",
        filterset_class=filters.EmployeeStatusFilter,
    )
    
    def resolve_employee_status(self, info, **data):
        id = data.get("id")
        return resolve_employee_status(id)
    
    def resolve_employee_statuses(self, info, **_kwargs):
        return resolve_employee_statuses()


class RegionQuery(graphene.ObjectType):
    region = graphene.Field(
        RegionNode,
        description = "Look up a region by ID.",
        id = graphene.Argument(graphene.ID, description="ID for a region", required=True)
    )
    all_regions = DjangoFilterConnectionField(
        RegionNode,
        description = "List of regions.",
        filterset_class=filters.RegionFilter,
    )
    
    def resolve_region(self, info, **data):
        id = data.get("id")
        return resolve_region(id)
    
    def resolve_regions(self, info, **_kwargs):
        return resolve_regions()

    
class UserQuery(graphene.ObjectType):
    user = graphene.Field(
        UserNode,
        description = "Look up a user by ID.",
        id = graphene.Argument(graphene.ID, description="ID for a user", required=True)
    )
    all_users = DjangoFilterConnectionField(
        UserNode,
        description = "List of users.",
        filterset_class=filters.UserFilter,
    )
    
    def resolve_user(self, info, **data):
        id = data.get("id")
        return resolve_user(id)
    
    def resolve_users(self, info, **_kwargs):
        return resolve_users()