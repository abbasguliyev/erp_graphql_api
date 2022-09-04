import graphene
from django_graphene_permissions import permissions_checker
from api.product.types import (
    CreateCategoryInput,
    UpdateCategoryInput,
    CategoryNode
)
from product.models import Category

from api.product.permissions import (
    category_permissions,
)

class CreateCategory(graphene.Mutation):
    class Arguments:
        input = CreateCategoryInput(
            required=True, description="Fields required to create category"
        )

    category = graphene.Field(CategoryNode)
    message = graphene.String()

    class Meta:
        description = "Create new Category"
        model = Category

    @permissions_checker([category_permissions.CategoryCreatePermissions])
    def mutate(root, info, input):
        category = Category()
        category.category_name = input.get("category_name")
        category.save()

        message = "Category created"
        return CreateCategory(category=category, message=message)


class UpdateCategory(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True, description="ID of a category")
        input = UpdateCategoryInput(
            required=True, description="Fields required to Update category"
        )

    category = graphene.Field(CategoryNode)
    message = graphene.String()

    class Meta:
        description = "Update Category"
        model = Category

    @permissions_checker([category_permissions.CategoryUpdatePermissions])
    def mutate(root, info, input):
        Category.objects.filter(pk=id).update(**input)
        category = Category.objects.get(pk=id)
        message = "Category Updated"
        return UpdateCategory(category=category, message=message)


class DeleteCategory(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True, description="ID of a category")

    message = graphene.String()

    class Meta:
        description = "Delete Category"
        model = Category

    @permissions_checker([category_permissions.CategoryDeletePermissions])
    def mutate(root, info, id):
        category = Category.objects.get(pk=id).delete()
        message = "Category deleted"
        return DeleteCategory(message=message)
