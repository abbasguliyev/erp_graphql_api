import graphene
from graphene_django.filter import DjangoFilterConnectionField

from api.account.mutations import (
    customer_mutations,
    customer_note_mutations,
    employee_status_mutations,
    region_mutations,
    user_mutations
)

from . import filters
from .resolvers import (
    resolve_customers,
    resolve_cutomer,
    resolve_cutomer_notes,
    resolve_cutomer_note,
    resolve_employee_status,
    resolve_employee_statuses,
    resolve_group,
    resolve_groups,
    resolve_permission,
    resolve_permissions,
    resolve_regions,
    resolve_region,
    resolve_users,
    resolve_user
)
from .types import (
    CustomerNode,
    CustomerNoteNode,
    EmployeeStatusNode,
    GroupNode,
    PermissionNode,
    RegionNode,
    CustomUserNode
)
from graphql_auth import mutations

from . import filters

from django_graphene_permissions import permissions_checker
from api.account.permissions.user_permissions import UserReadPermissions
from api.account.permissions.customer_permissions import CustomerReadPermissions
from api.account.permissions.customer_note_permissions import CustomerNoteReadPermissions
from api.account.permissions.region_permissions import RegionReadPermissions
from api.account.permissions.employee_status_permissions import EmployeeStatusReadPermissions
from core.permissions import IsAdminUser

class PermissionQuery(graphene.ObjectType):
    permission = graphene.Field(PermissionNode, description="Look up a permission by ID.",
                                id=graphene.Argument(graphene.ID, description="ID for a permission", required=True))

    permissions = DjangoFilterConnectionField(
        PermissionNode,
        description="List of permissions.",
        filterset_class=filters.PermissionFilter,
    )
    
    @permissions_checker([IsAdminUser])
    def resolve_permission(self, info, **data):
        id = data.get("id")
        return resolve_permission(id)
    
    @permissions_checker([IsAdminUser])
    def resolve_permissions(self, info, **_kwargs):
        return resolve_permissions()
        
class GroupQuery(graphene.ObjectType):
    group = graphene.Field(GroupNode, description="Look up a group by ID.",
                                id=graphene.Argument(graphene.ID, description="ID for a group", required=True))

    groups = DjangoFilterConnectionField(
        GroupNode,
        description="List of groups.",
        filterset_class=filters.GroupFilter,
    )
    
    @permissions_checker([IsAdminUser])
    def resolve_group(self, info, **data):
        id = data.get("id")
        return resolve_group(id)

    @permissions_checker([IsAdminUser])
    def resolve_groups(self, info, **_kwargs):
        return resolve_groups()
        
        
        
class CustomerQuery(graphene.ObjectType):
    customer = graphene.Field(
        CustomerNode,
        description="Look up a customer by ID.",
        id=graphene.Argument(
            graphene.ID, description="ID for a customer", required=True)
    )
    customers = DjangoFilterConnectionField(
        CustomerNode,
        description="List of customers.",
        filterset_class=filters.CustomerFilter,
    )

    @permissions_checker([CustomerReadPermissions])
    def resolve_customer(self, info, **data):
        id = data.get("id")
        return resolve_cutomer(id)
    
    @permissions_checker([CustomerReadPermissions])
    def resolve_customers(self, info, **_kwargs):
        return resolve_customers()


class CustomerNoteQuery(graphene.ObjectType):
    customer_note = graphene.Field(
        CustomerNoteNode,
        description="Look up a customer note by ID.",
        id=graphene.Argument(
            graphene.ID, description="ID for a customer note", required=True)
    )
    customer_notes = DjangoFilterConnectionField(
        CustomerNoteNode,
        description="List of customer notes.",
        filterset_class=filters.CustomerNoteFilter,
    )

    @permissions_checker([CustomerNoteReadPermissions])
    def resolve_customer_note(self, info, **data):
        id = data.get("id")
        return resolve_cutomer_note(id)

    @permissions_checker([CustomerNoteReadPermissions])
    def resolve_customer_notes(self, info, **_kwargs):
        return resolve_cutomer_notes()


class EmployeeStatusQuery(graphene.ObjectType):
    employee_status = graphene.Field(
        EmployeeStatusNode,
        description="Look up a employee status by ID.",
        id=graphene.Argument(
            graphene.ID, description="ID for a employee status", required=True)
    )
    employee_statuses = DjangoFilterConnectionField(
        EmployeeStatusNode,
        description="List of employee statuses.",
        filterset_class=filters.EmployeeStatusFilter,
    )

    @permissions_checker([EmployeeStatusReadPermissions])
    def resolve_employee_status(self, info, **data):
        id = data.get("id")
        return resolve_employee_status(id)

    @permissions_checker([EmployeeStatusReadPermissions])
    def resolve_employee_statuses(self, info, **_kwargs):
        return resolve_employee_statuses()


class RegionQuery(graphene.ObjectType):
    region = graphene.Field(
        RegionNode,
        description="Look up a region by ID.",
        id=graphene.Argument(
            graphene.ID, description="ID for a region", required=True)
    )
    regions = DjangoFilterConnectionField(
        RegionNode,
        description="List of regions.",
        filterset_class=filters.RegionFilter,
    )

    @permissions_checker([RegionReadPermissions])
    def resolve_region(self, info, **data):
        id = data.get("id")
        return resolve_region(id)

    @permissions_checker([RegionReadPermissions])
    def resolve_regions(self, info, **_kwargs):
        return resolve_regions()


class UserQuery(graphene.ObjectType):
    user = graphene.Field(
        CustomUserNode,
        description="Look up a user by ID.",
        id=graphene.Argument(
            graphene.ID, description="ID for a user", required=True)
    )
    users = DjangoFilterConnectionField(
        CustomUserNode,
        description="List of users.",
        filterset_class=filters.UserFilter,
    )

    @permissions_checker([UserReadPermissions])
    def resolve_user(self, info, **data):
        id = data.get("id")
        return resolve_user(id)
    
    @permissions_checker([UserReadPermissions])
    def resolve_users(self, info, **_kwargs):
        return resolve_users()

# ----------------------- Mutations ---------------------------------------

class UserMutations(graphene.ObjectType):
    create_user = user_mutations.CreateUser.Field()
    verify_account = mutations.VerifyAccount.Field()
    token_auth = mutations.ObtainJSONWebToken.Field()
    update_user = user_mutations.UpdateUser.Field()
    delete_user = user_mutations.DeleteUser.Field()
    change_password = user_mutations.ChangePassword.Field()
    reset_password = user_mutations.ResetPassword.Field()
    create_group = user_mutations.CreateGroup.Field()
    update_group = user_mutations.UpdateGroup.Field()
    delete_group = user_mutations.DeleteGroup.Field()



class CustomerMutations(graphene.ObjectType):
    create_customer = customer_mutations.CreateCustomer.Field()
    update_customer = customer_mutations.UpdateCustomer.Field()
    delete_customer = customer_mutations.DeleteCustomer.Field()


class CustomerNoteMutations(graphene.ObjectType):
    create_customer_note = customer_note_mutations.CreateCustomerNote.Field()
    update_customer_note = customer_note_mutations.UpdateCustomerNote.Field()
    delete_customer_note = customer_note_mutations.DeleteCustomerNote.Field()


class EmployeeStatusMutations(graphene.ObjectType):
    create_employee_status = employee_status_mutations.CreateEmployeeStatus.Field()
    update_employee_status = employee_status_mutations.UpdateEmployeeStatus.Field()
    delete_employee_status = employee_status_mutations.DeleteEmployeeStatus.Field()


class RegionMutations(graphene.ObjectType):
    create_all_region = region_mutations.AllRegionCreate.Field()
    create_region = region_mutations.CreateRegion.Field()
    update_region = region_mutations.UpdateRegion.Field()
    delete_region = region_mutations.DeleteRegion.Field()