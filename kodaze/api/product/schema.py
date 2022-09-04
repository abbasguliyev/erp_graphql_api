import graphene
from graphene_django.filter import DjangoFilterConnectionField

from .mutations import unit_of_measure_mutations

from . import filters

from .resolvers import (
    resolve_categories,
    resolve_category,
    resolve_product,
    resolve_products,
    resolve_unit_of_measure,
    resolve_unit_of_measures
)

from . types import (
    ProductNode,
    CategoryNode,
    UnitOfMeasureNode,
)

from .mutations import (
    category_mutations,
    unit_of_measure_mutations
)

from django_graphene_permissions import permissions_checker
from .permissions import (
    category_permissions,
    product_permissions,
    unit_of_measure_permissions
)


class ProductQuery(graphene.ObjectType):
    product = graphene.Field(ProductNode, description="Look up a product by ID.",
                             id=graphene.Argument(graphene.ID, description="ID for a product", required=True))

    products = DjangoFilterConnectionField(
        ProductNode,
        description="List of product.",
        filterset_class=filters.ProductFilter,
    )

    @permissions_checker([product_permissions.ProductReadPermissions])
    def resolve_product(self, info, **data):
        id = data.get("id")
        return resolve_product(id)

    @permissions_checker([product_permissions.ProductReadPermissions])
    def resolve_products(self, info, **_kwargs):
        return resolve_products()


class CategoryQuery(graphene.ObjectType):
    category = graphene.Field(CategoryNode, description="Look up a category by ID.",
                              id=graphene.Argument(graphene.ID, description="ID for a category", required=True))

    categories = DjangoFilterConnectionField(
        CategoryNode,
        description="List of category.",
        filterset_class=filters.CategoryFilter,
    )

    @permissions_checker([category_permissions.CategoryReadPermissions])
    def resolve_category(self, info, **data):
        id = data.get("id")
        return resolve_category(id)

    @permissions_checker([category_permissions.CategoryReadPermissions])
    def resolve_categories(self, info, **_kwargs):
        return resolve_categories()


class UnitOfMeasureQuery(graphene.ObjectType):
    unit_of_measure = graphene.Field(UnitOfMeasureNode, description="Look up a unit_of_measure by ID.",
                                     id=graphene.Argument(graphene.ID, description="ID for a unit_of_measure", required=True))

    unit_of_measures = DjangoFilterConnectionField(
        UnitOfMeasureNode,
        description="List of unit_of_measure.",
        filterset_class=filters.UnitOfMeasure,
    )

    @permissions_checker([unit_of_measure_permissions.OfficeReadPermissions])
    def resolve_unit_of_measure(self, info, **data):
        id = data.get("id")
        return resolve_unit_of_measure(id)

    @permissions_checker([unit_of_measure_permissions.OfficeReadPermissions])
    def resolve_unit_of_measures(self, info, **_kwargs):
        return resolve_unit_of_measures()

# ----------------------- Mutations ---------------------------------------


class ProductMutations(graphene.ObjectType):
    create_product = unit_of_measure_mutations.CreateProduct.Field()
    update_product = unit_of_measure_mutations.UpdateProduct.Field()
    delete_product = unit_of_measure_mutations.DeleteProduct.Field()


class CategoryMutations(graphene.ObjectType):
    create_category = category_mutations.CreateCategory.Field()
    update_category = category_mutations.UpdateCategory.Field()
    delete_category = category_mutations.DeleteCategory.Field()


class UnitOfMeasureMutations(graphene.ObjectType):
    create_unit_of_measure = unit_of_measure_mutations.CreateUnitOfMeasure.Field()
    update_unit_of_measure = unit_of_measure_mutations.UpdateUnitOfMeasure.Field()
    delete_unit_of_measure = unit_of_measure_mutations.DeleteUnitOfMeasure.Field()
