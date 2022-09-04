import graphene
from graphene import relay, InputObjectType
from graphene_django import DjangoObjectType
from api.company.types import CompanyNode
from product.models import Product, Category, UnitOfMeasure
from core import values


class ProductNode(DjangoObjectType):
    class Meta:
        model = Product
        interfaces = (relay.Node, )


class CategoryNode(DjangoObjectType):
    class Meta:
        model = Category
        interfaces = (relay.Node, )


class UnitOfMeasureNode(DjangoObjectType):
    class Meta:
        model = UnitOfMeasure
        interfaces = (relay.Node, )


class CreateProductInput(InputObjectType):
    product_name = graphene.String(required=True, description="product name")
    company = graphene.ID(CompanyNode, required=True,
                          description="product company")
    category = graphene.ID(CategoryNode, required=True,
                           description="product category")
    price = graphene.Decimal(required=True, description="product price")
    unit_of_measure = graphene.ID(
        UnitOfMeasureNode, required=True, description="product unit of measure")
    volume = graphene.Float(required=False, description="product volume")
    weight = graphene.Float(required=False, description="product weight")
    width = graphene.Float(required=False, description="product width")
    length = graphene.Float(required=False, description="product length")
    height = graphene.Float(required=False, description="product height")
    note = graphene.String(required=False, description="product note")
    product_image = values.Upload(required=False, description="product image")
    is_gift = graphene.Boolean(required=False, description="Is gift")


class UpdateProductInput(InputObjectType):
    product_name = graphene.String(required=False, description="product name")
    company = graphene.ID(CompanyNode, required=False,
                          description="product company")
    category = graphene.ID(CategoryNode, required=False,
                           description="product category")
    price = graphene.Decimal(required=False, description="product price")
    unit_of_measure = graphene.ID(
        UnitOfMeasureNode, required=False, description="product unit of measure")
    volume = graphene.Float(required=False, description="product volume")
    weight = graphene.Float(required=False, description="product weight")
    width = graphene.Float(required=False, description="product width")
    length = graphene.Float(required=False, description="product length")
    height = graphene.Float(required=False, description="product height")
    note = graphene.String(required=False, description="product note")
    product_image = values.Upload(required=False, description="product image")
    is_gift = graphene.Boolean(required=False, description="Is gift")


class CreateCategoryInput(InputObjectType):
    category_name = graphene.String(required=True, description="category_name")


class UpdateCategoryInput(InputObjectType):
    category_name = graphene.String(
        required=False, description="category_name")


class CreateUnitOfMeasureInput(InputObjectType):
    name = graphene.String(required=True, description="name")


class UpdateUnitOfMeasureInput(InputObjectType):
    name = graphene.String(required=False, description="name")
