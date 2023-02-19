import graphene

from api.account.types import (
    CreateCustomerNoteInput,
    CustomerNoteNode,
    UpdateCustomerNoteInput,
)

from account.models import (
    CustomerNote,
)

from django_graphene_permissions import permissions_checker
from api.account.permissions.customer_note_permissions import (
    CustomerNoteCreatePermissions,
    CustomerNoteUpdatePermissions,
    CustomerNoteDeletePermissions
)

class CreateCustomerNote(graphene.Mutation):
    class Arguments:
        input = CreateCustomerNoteInput(
            required=True, description="Fields required to create customer note"
        )

    customer_note = graphene.Field(CustomerNoteNode)
    message = graphene.String()

    class Meta:
        description = "Create new Customer note"
        model = CustomerNote

    @permissions_checker([CustomerNoteCreatePermissions])
    def mutate(root, info, input):
        customer_note = CustomerNote()
        customer_note.note = input.get("note")
        customer_note.customer = input.get("customer")
        customer_note.save()
        message = "Customer note created"
        return CreateCustomerNote(customer_note=customer_note, message=message)


class UpdateCustomerNote(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True, description="ID of a customer note")
        input = UpdateCustomerNoteInput(
            required=True, description="Fields required to Update Customer note")

    customer_note = graphene.Field(CustomerNoteNode)
    message = graphene.String()

    class Meta:
        description = "Update Customer note"
        model = CustomerNote

    @permissions_checker([CustomerNoteUpdatePermissions])
    def mutate(root, info, input, id):
        CustomerNote.objects.filter(pk=id).update(**input)
        customer_note = CustomerNote.objects.get(pk=id)
        message = "Customer note updated"
        return UpdateCustomerNote(customer_note=customer_note, message=message)


class DeleteCustomerNote(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True, description="ID of a customer note")

    class Meta:
        description = "Delete Customer note"
        model = CustomerNote
    message = graphene.String()

    @permissions_checker([CustomerNoteDeletePermissions])
    def mutate(root, info, id):
        customer = CustomerNote.objects.get(pk=id).delete()
        message = "Customer note deleted"
        return DeleteCustomerNote(message=message)
