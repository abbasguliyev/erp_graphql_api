import graphene
from django_graphene_permissions import permissions_checker
from api.product.types import (
    CreateProductInput,
    UpdateProductInput,
    ProductNode
)
from company.models import Company
from product.models import Category, UnitOfMeasure, Product

from api.product.permissions import (
    product_permissions,
)

class CreateProduct(graphene.Mutation):
    class Arguments:
        input = CreateProductInput(
            required=True, description="Fields required to create product"
        )

    product = graphene.Field(ProductNode)
    message = graphene.String()

    class Meta:
        description = "Create new Product"
        model = Product

    @permissions_checker([product_permissions.ProductCreatePermissions])
    def mutate(root, info, input):
        company_id = input.get('company')
        company = Company.objects.select_related('holding').get(pk=company_id)
        
        category_id = input.get('category')
        category = Category.objects.get(pk=category_id)
        
        unit_of_measure_id = input.get('unit_of_measure')
        unit_of_measure = UnitOfMeasure.objects.get(pk=unit_of_measure_id)
        
        try:
            product_image = input.get('product_image')
        except:
            product_image = None
        
        product = Product()
        product.product_name = input.get("product_name")
        product.company = company
        product.category = category
        product.price = input.get("price")
        product.unit_of_measure = unit_of_measure
        product.volume = input.get("volume")
        product.weight = input.get("weight")
        product.width = input.get("width")
        product.length = input.get("length")
        product.height = input.get("height")
        product.note = input.get("note")
        product.product_image = product_image
        product.is_gift = input.get("is_gift")
        product.save()

        message = "Product created"
        return CreateProduct(product=product, message=message)


class UpdateProduct(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True, description="ID of a product")
        input = UpdateProductInput(
            required=True, description="Fields required to Update product"
        )

    product = graphene.Field(ProductNode)
    message = graphene.String()

    class Meta:
        description = "Update Product"
        model = Product

    @permissions_checker([product_permissions.ProductUpdatePermissions])
    def mutate(root, info, input):
        Product.objects.filter(pk=id).update(**input)
        product = Product.objects.get(pk=id)
        message = "Product Updated"
        return UpdateProduct(product=product, message=message)


class DeleteProduct(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True, description="ID of a product")

    message = graphene.String()

    class Meta:
        description = "Delete Product"
        model = Product

    @permissions_checker([product_permissions.ProductDeletePermissions])
    def mutate(root, info, id):
        product = Product.objects.get(pk=id).delete()
        message = "Product deleted"
        return DeleteProduct(message=message)
