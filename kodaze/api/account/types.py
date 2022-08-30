from django.contrib.auth.models import Permission, Group
from django.contrib.auth import get_user_model
import graphene
from graphene import relay, InputObjectType
from graphene_django import DjangoObjectType
from account.models import (
    Customer,
    CustomerNote,
    EmployeeStatus,
    Region,
)
from api.core import values

User = get_user_model()


class CustomerNode(DjangoObjectType):
    class Meta:
        model = Customer
        interfaces = (relay.Node, )


class CustomerNoteNode(DjangoObjectType):
    class Meta:
        model = CustomerNote
        interfaces = (relay.Node, )


class CreateCustomerInput(InputObjectType):
    first_name = graphene.String(
        required=True, description="Customer first name")
    last_name = graphene.String(
        required=True, description="Customer last name")
    father_name = graphene.String(
        required=True, description="Customer father name")
    profile_image = values.Upload(
        required=False, description="Customer profile image")
    photo_ID = values.Upload(
        required=False, description="Customer ID card image")
    back_photo_of_ID = values.Upload(
        required=False, description="Customer ID card back image")
    phone_number_1 = graphene.String(
        required=True, description="Customer phone number")
    phone_number_2 = graphene.String(
        required=False, description="Customer phone number")
    phone_number_3 = graphene.String(
        required=False, description="Customer phone number")
    email = graphene.String(required=False, description="Customer email")
    address = graphene.String(required=True, description="Customer address")
    region = graphene.ID(required=True, description="Customer region")
    note = graphene.String(required=False, description="Customer note")
    customer_type = graphene.String(required=True, description="Customer type")


class UpdateCustomerInput(InputObjectType):
    first_name = graphene.String(
        required=False, description="Customer first name")
    last_name = graphene.String(
        required=False, description="Customer last name")
    father_name = graphene.String(
        required=False, description="Customer father name")
    profile_image = values.Upload(
        required=False, description="Customer profile image")
    photo_ID = values.Upload(
        required=False, description="Customer ID card image")
    back_photo_of_ID = values.Upload(
        required=False, description="Customer ID card back image")
    phone_number_1 = graphene.String(
        required=False, description="Customer phone number")
    phone_number_2 = graphene.String(
        required=False, description="Customer phone number")
    phone_number_3 = graphene.String(
        required=False, description="Customer phone number")
    email = graphene.String(required=False, description="Customer email")
    address = graphene.String(required=False, description="Customer address")
    region = graphene.ID(required=False, description="Customer region")
    note = graphene.String(required=False, description="Customer note")
    customer_type = graphene.String(
        required=False, description="Customer type")


class CreateCustomerNoteInput(InputObjectType):
    note = graphene.String(required=True, description="Customer note")
    customer = graphene.ID(required=True, description="Customer id")


class UpdateCustomerNoteInput(InputObjectType):
    note = graphene.String(required=False, description="Customer note")
    customer = graphene.ID(required=False, description="Customer id")


class EmployeeStatusNode(DjangoObjectType):
    class Meta:
        model = EmployeeStatus
        interfaces = (relay.Node, )


class CreateEmployeeStatusInput(InputObjectType):
    status_name = graphene.String(
        required=True, description="Employee status name")


class UpdateEmployeeStatusInput(InputObjectType):
    status_name = graphene.String(
        required=False, description="Employee status name")


class RegionNode(DjangoObjectType):
    class Meta:
        model = Region
        interfaces = (relay.Node, )


class CreateRegionInput(InputObjectType):
    region_name = graphene.String(required=True, description="Region name")


class UpdateRegionInput(InputObjectType):
    region_name = graphene.String(required=False, description="Region name")


class PermissionNode(DjangoObjectType):
    class Meta:
        model = Permission
        interfaces = (relay.Node,)


class GroupNode(DjangoObjectType):
    class Meta:
        model = Group
        interfaces = (relay.Node,)


class CustomUserNode(DjangoObjectType):
    class Meta:
        model = User
        filter_fields = ['first_name']
        interfaces = (relay.Node, )


class CreateUserInput(InputObjectType):
    first_name = graphene.String(required=True, description="User first name")
    last_name = graphene.String(required=True, description="User last name")
    username = graphene.String(required=True, description="User username")
    email = graphene.String(required=False, description="User email")
    date_of_birth = graphene.Date(
        required=True, format="%d-%m-%Y", description="User date of birth")
    start_date_of_work = graphene.Date(
        required=False, description="User start date of work")
    dismissal_date = graphene.Date(
        required=False, description="User dismissal date")
    phone_number_1 = graphene.String(
        required=True, description="User phone number")
    phone_number_2 = graphene.String(
        required=False, description="User phone number")
    profile_image = values.Upload(
        required=False, description="User profile image")
    photo_ID = values.Upload(required=False, description="User ID card image")
    back_photo_of_ID = values.Upload(
        required=False, description="User ID card back image")
    driving_license_photo = values.Upload(
        required=False, description="User driving license photo")
    company = graphene.ID(required=False, default=None,
                          description="User company")
    office = graphene.ID(required=False, default=None,
                         description="User office")
    department = graphene.ID(required=False, default=None,
                             description="User department")
    position = graphene.ID(required=False, default=None,
                           description="User position")
    team = graphene.ID(required=False, default=None, description="User team")
    employee_status = graphene.ID(
        required=False, default=None, description="User employee status")
    salary_style = graphene.String(
        required=True, description="User salary type")
    contract_type = graphene.String(
        required=True, description="User contract type")
    salary = graphene.Decimal(required=False, description="User salary")
    note = graphene.String(required=False, description="User note")
    password = graphene.String(required=True, description="User password")
    supervisor = graphene.ID(required=False, description="User supervisor")


class UpdateUserInput(InputObjectType):
    first_name = graphene.String(required=False, description="User first name")
    last_name = graphene.String(required=False, description="User last name")
    username = graphene.String(required=False, description="User username")
    email = graphene.String(required=False, description="User email")
    date_of_birth = graphene.Date(
        required=False, description="User date of birth")
    start_date_of_work = graphene.Date(
        required=False, description="User start date of work")
    dismissal_date = graphene.Date(
        required=False, description="User dismissal date")
    phone_number_1 = graphene.String(
        required=False, description="User phone number")
    phone_number_2 = graphene.String(
        required=False, description="User phone number")
    profile_image = values.Upload(
        required=False, description="User profile image")
    photo_ID = values.Upload(required=False, description="User ID card image")
    back_photo_of_ID = values.Upload(
        required=False, description="User ID card back image")
    driving_license_photo = values.Upload(
        required=False, description="User driving license photo")
    company = graphene.ID(required=False, description="User company")
    office = graphene.ID(required=False, description="User office")
    department = graphene.ID(required=False, description="User department")
    position = graphene.ID(required=False, description="User position")
    team = graphene.ID(required=False, description="User team")
    employee_status = graphene.ID(
        required=False, description="User employee status")
    salary_style = graphene.String(
        required=False, description="User salary type")
    contract_type = graphene.String(
        required=False, description="User contract type")
    salary = graphene.Decimal(required=False, description="User salary")
    note = graphene.String(required=False, description="User note")
    supervisor = graphene.ID(required=False, description="User supervisor")


class CreateGroupInput(InputObjectType):
    name = graphene.String(required=True, desctription="Group name")
    permissions = graphene.List(graphene.ID, required=True)


class UpdateGroupInput(InputObjectType):
    name = graphene.String(required=False, desctription="Group name")
    permissions = graphene.List(graphene.ID, required=False)


class ChangePasswordInput(InputObjectType):
    old_password = graphene.String(required=True)
    new_password = graphene.String(required=True)


class ResetPasswordInput(InputObjectType):
    username = graphene.String(required=True)
    new_password = graphene.String(required=True)
