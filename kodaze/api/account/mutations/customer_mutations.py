import graphene

from api.account.types import (
    CustomerNode,
    CreateCustomerInput,
    UpdateCustomerInput,
)

from account.models import (
    Customer,
    Region,
)
from django.contrib.auth import get_user_model

from django_graphene_permissions import permissions_checker
from api.account.permissions.customer_permissions import (
    CustomerCreatePermissions,
    CustomerUpdatePermissions,
    CustomerDeletePermissions,
)
User = get_user_model()


class CreateCustomer(graphene.Mutation):
    class Arguments:
        input = CreateCustomerInput(
            required=True, description="Fields required to create customer"
        )

    customer = graphene.Field(CustomerNode)
    message = graphene.String()

    class Meta:
        description = "Create new Customer"
        model = Customer

    @permissions_checker([CustomerCreatePermissions])
    def mutate(root, info, input):
        region_id = input.get("region")
        region = Region.objects.filter(id=region_id).first()
        try:
            profile_image = info.context.FILES[input.get("profile_image")]
        except:
            profile_image = None
        try:
            photo_ID = info.context.FILES[input.get("photo_ID")]
        except:
            photo_ID = None
        try:
            back_photo_of_ID = info.context.FILES[input.get(
                "back_photo_of_ID")]
        except:
            back_photo_of_ID = None
        customer = Customer()
        customer.first_name = input.get("first_name")
        customer.last_name = input.get("last_name")
        customer.father_name = input.get("father_name")
        customer.profile_image = profile_image
        customer.photo_ID = photo_ID
        customer.back_photo_of_ID = back_photo_of_ID
        customer.phone_number_1 = input.get("phone_number_1")
        customer.phone_number_2 = input.get("phone_number_2")
        customer.phone_number_3 = input.get("phone_number_3")
        customer.email = input.get("email")
        customer.address = input.get("address")
        customer.region = region
        customer.note = input.get("note")
        customer.executor = info.context.user
        customer.customer_type = input.get("customer_type")
        customer.save()
        message = "Customer created"
        return CreateCustomer(customer=customer, message=message)


class UpdateCustomer(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True, description="ID of a customer")
        input = UpdateCustomerInput(
            required=True, description="Fields required to Update Customer")

    customer = graphene.Field(CustomerNode)
    message = graphene.String()

    class Meta:
        description = "Update Customer"
        model = Customer

    @permissions_checker([CustomerUpdatePermissions])
    def mutate(root, info, input, id):
        Customer.objects.filter(pk=id).update(**input)
        customer = Customer.objects.get(pk=id)
        message = "Customer updated"
        return UpdateCustomer(customer=customer, message=message)


class DeleteCustomer(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True, description="ID of a customer")

    message = graphene.String()

    class Meta:
        description = "Delete Customer"
        model = Customer

    @permissions_checker([CustomerDeletePermissions])
    def mutate(root, info, id):
        Customer.objects.get(pk=id).delete()
        message = "Customer deleted"
        return DeleteCustomer(message=message)
