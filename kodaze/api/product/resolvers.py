from product.models import Product, Category, UnitOfMeasure


def resolve_product(id):
    return Product.objects.select_related('company', 'category', 'unit_of_measure').get(id=id)


def resolve_products():
    return Product.objects.select_related('company', 'category', 'unit_of_measure').all()


def resolve_category(id):
    return Category.objects.get(id=id)


def resolve_categories():
    return Category.objects.all()


def resolve_unit_of_measure(id):
    return UnitOfMeasure.objects.get(id=id)


def resolve_unit_of_measures():
    return UnitOfMeasure.objects.all()
