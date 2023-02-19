import graphene
from django_graphene_permissions import permissions_checker
from company.models import Department, Office
from api.company.types import (
    CreateDepartmentInput,
    UpdateDepartmentInput,
    DepartmentNode
)

from api.company.permissions import (
    department_permissions,
)


class CreateDepartment(graphene.Mutation):
    class Arguments:
        input = CreateDepartmentInput(
            required=True, description="Fields required to create department"
        )

    department = graphene.Field(DepartmentNode)
    message = graphene.String()

    class Meta:
        description = "Create new Department"
        model = Department

    @permissions_checker([department_permissions.DepartmentCreatePermissions])
    def mutate(root, info, input):
        office_id = input.get("office")
        office = Office.objects.get(pk=office_id)

        department = Department()
        department.name = input.get("name")
        department.office = office
        department.save()
        message = "Department created"
        return CreateDepartment(department=department, message=message)


class UpdateDepartment(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True, description="ID of a department")
        input = UpdateDepartmentInput(
            required=True, description="Fields required to Update department"
        )

    department = graphene.Field(DepartmentNode)
    message = graphene.String()

    class Meta:
        description = "Update Department"
        model = Department

    @permissions_checker([department_permissions.DepartmentUpdatePermissions])
    def mutate(root, info, input):
        Department.objects.filter(pk=id).update(**input)
        department = Department.objects.get(pk=id)
        message = "Department Updated"
        return UpdateDepartment(department=department, message=message)


class DeleteDepartment(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True, description="ID of a department")

    message = graphene.String()

    class Meta:
        description = "Delete Department"
        model = Department

    @permissions_checker([department_permissions.DepartmentDeletePermissions])
    def mutate(root, info, id):
        department = Department.objects.get(pk=id)
        department.is_active = False
        department.save()
        message = "Department deactivated"
        return DeleteDepartment(message=message)
