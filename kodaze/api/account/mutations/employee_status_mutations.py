import graphene

from api.account.types import (
    CreateEmployeeStatusInput,
    EmployeeStatusNode,
    UpdateEmployeeStatusInput,
)

from account.models import (
    EmployeeStatus,
)
from django_graphene_permissions import permissions_checker
from account.permissions.employee_status_permissions import (
    EmployeeStatusCreatePermissions,
    EmployeeStatusUpdatePermissions,
    EmployeeStatusDeletePermissions
)

class CreateEmployeeStatus(graphene.Mutation):
    class Arguments:
        input = CreateEmployeeStatusInput(
            required=True, description="Fields required to create employee status"
        )

    employee_status = graphene.Field(EmployeeStatusNode)
    message = graphene.String()
    class Meta:
        description = "Create new Employee Status"
        model = EmployeeStatus

    @permissions_checker([EmployeeStatusCreatePermissions])
    def mutate(root, info, input):
        employee_status = EmployeeStatus()
        employee_status.status_name = input.get("status_name")
        employee_status.save()
        message = "Employee status created"
        return CreateEmployeeStatus(employee_status=employee_status, message=message)


class UpdateEmployeeStatus(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True, description="ID of a employee status")
        input = UpdateEmployeeStatusInput(
            required=True, description="Fields required to Update Employee Status")

    employee_status = graphene.Field(EmployeeStatusNode)
    message = graphene.String()
    class Meta:
        description = "Update new Employee Status"
        model = EmployeeStatus

    @permissions_checker([EmployeeStatusUpdatePermissions])
    def mutate(root, info, input, id):
        EmployeeStatus.objects.filter(pk=id).update(**input)
        employee_status = EmployeeStatus.objects.get(pk=id)
        message = "Employee Status updated"
        return UpdateEmployeeStatus(employee_status=employee_status, message=message)

class DeleteEmployeeStatus(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True, description="ID of a employee status")

    class Meta:
        description = "Delete EmployeeStatus"
        model = EmployeeStatus
    message = graphene.String()
    
    @permissions_checker([EmployeeStatusDeletePermissions])
    def mutate(root, info, id):
        employee_status = EmployeeStatus.objects.get(pk=id).delete()
        message = "Employee Status deleted"
        return DeleteEmployeeStatus(message=message)
